from django.views.generic import (
    View, TemplateView, ListView, DetailView, 
    CreateView, UpdateView, FormView
)
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from product.models import Category, Product
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from users.models import User
from .forms import CustomUserCreationForm

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.models import VendorProfile  # Import VendorProfile model
from django.contrib import messages


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from vendor.models import VendorProfile
from product.models import Category, Product

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm  # You'll need to create this form
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from product.models import Product, Category
from vendor.models import VendorProfile
from django.core.exceptions import PermissionDenied

# Your models and forms imports remain the same

class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('check_user_role')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

# class UserSignupView(CreateView):
#     template_name = 'users/signup.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('users:check_user_role')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)
#         return response


class UserSignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:check_user_role')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        
        # Send verification email if user is a vendor
        if user.is_vendor():
            user.send_verification_email(self.request)
            messages.info(self.request, 'A verification email has been sent to your email address. Please verify your email to complete registration.')
            # Log the user out until they verify their email
            return redirect('users:verification_sent')
        
        login(self.request, user)
        return response







class CheckUserRoleView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_vendor():
                if not request.user.is_email_verified:
                    return redirect('users:verification_required')
                return redirect('vendor:dashboard')
            elif request.user.is_admin():
                return redirect('users:admin_dashboard')
            return redirect('home')
        return redirect('login')
    
class VerificationSentView(TemplateView):
    template_name = 'users/verification_sent.html'
    
class VerificationRequiredView(LoginRequiredMixin, TemplateView):
    template_name = 'users/verification_required.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_vendor() or request.user.is_email_verified:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            user = User.objects.get(email_verification_token=token)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.email_verification_token = ''
                user.save()
                messages.success(request, 'Your email has been verified successfully! You can now login.')
                return redirect('users:login')
            else:
                messages.info(request, 'Your email is already verified.')
                return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid verification token.')
            return redirect('users:login')
        
        
class ResendVerificationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_vendor() or request.user.is_email_verified:
            raise PermissionDenied
        
        request.user.send_verification_email(request)
        messages.info(request, 'A new verification email has been sent to your email address.')
        return redirect('users:verification_sent')
        
        
        
        

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_admin()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_count'] = VendorProfile.objects.count()
        context['product_count'] = Product.objects.count()
        context['recent_vendors'] = VendorProfile.objects.select_related('user').order_by('-user__date_joined')[:5]
        return context

class VendorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VendorProfile
    template_name = 'users/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(store_name__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(address__icontains=search_query))
        
        # Filter
        approval_filter = self.request.GET.get('is_approved', '')
        if approval_filter in ['true', 'false']:
            queryset = queryset.filter(is_approved=(approval_filter == 'true'))
        
        # Sort
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['store_name', '-store_name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_sort'] = self.request.GET.get('sort', '-created_at')
        context['selected_approval'] = self.request.GET.get('is_approved', '')
        return context

class VendorDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = VendorProfile
    template_name = 'users/vendor_detail.html'
    context_object_name = 'vendor'

    def test_func(self):
        return self.request.user.is_admin()

class ApproveVendorView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_admin()

    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(VendorProfile, pk=kwargs['pk'])
        vendor.is_approved = True
        vendor.save()
        messages.success(request, f'{vendor.store_name} has been approved!')
        return redirect('users:vendor_detail', pk=kwargs['pk'])

class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'users/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'category__vendor')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(category__vendor__store_name__icontains=search_query))
        
        # Filters
        category_filter = self.request.GET.get('category', '')
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        
        vendor_filter = self.request.GET.get('vendor', '')
        if vendor_filter:
            queryset = queryset.filter(category__vendor__id=vendor_filter)
        
        available_filter = self.request.GET.get('available', '')
        if available_filter in ['true', 'false']:
            queryset = queryset.filter(available=(available_filter == 'true'))
        
        # Sort
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['name', '-name', 'price', '-price', 'stock', '-stock', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['vendors'] = VendorProfile.objects.filter(is_approved=True)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_vendor'] = self.request.GET.get('vendor', '')
        context['selected_availability'] = self.request.GET.get('available', '')
        context['selected_sort'] = self.request.GET.get('sort', '-created_at')
        return context

class ProductDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'users/product_detail.html'
    context_object_name = 'product'

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'category__vendor')

class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'users/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vendor')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(vendor__store_name__icontains=search_query))
        
        # Filter
        vendor_filter = self.request.GET.get('vendor', '')
        if vendor_filter:
            queryset = queryset.filter(vendor__id=vendor_filter)
        
        # Sort
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = VendorProfile.objects.filter(is_approved=True)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_vendor'] = self.request.GET.get('vendor', '')
        context['selected_sort'] = self.request.GET.get('sort', '-created_at')
        return context

class CategoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Category
    template_name = 'users/category_detail.html'
    context_object_name = 'category'

    def test_func(self):
        return self.request.user.is_admin()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/edit_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile was successfully updated!')
        return super().form_valid(form)
    