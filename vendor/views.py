from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import VendorProfileForm
from users.models import User
from .models import VendorProfile


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()


class VendorDashboardView(LoginRequiredMixin, View):
    template_name = 'vendor/dashboard.html'
    
    def get(self, request):
        if not request.user.is_vendor():
            return redirect('home')
        
         # Check if email is verified
        if not request.user.is_email_verified:
            messages.warning(request, 'You must verify your email before accessing the vendor dashboard.')
            return redirect('users:verification_required')
        
        try:
            vendor_profile = request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return redirect('vendor:complete_profile')
        
        return render(request, self.template_name, {'vendor': vendor_profile})


class CompleteProfileView(LoginRequiredMixin, View):
    template_name = 'vendor/complete_profile.html'
    form_class = VendorProfileForm
    
    def get(self, request):
        if not request.user.is_vendor():
            return redirect('home')
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if not request.user.is_vendor():
            return redirect('home')
        
        form = self.form_class(request.POST)
        if form.is_valid():
            vendor_profile = form.save(commit=False)
            vendor_profile.user = request.user
            vendor_profile.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('vendor:dashboard')
        
        return render(request, self.template_name, {'form': form})


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'vendor/edit_profile.html'
    form_class = VendorProfileForm
    
    def get(self, request):
        if not request.user.is_vendor():
            return redirect('home')
        
        vendor_profile = request.user.vendor_profile
        form = self.form_class(instance=vendor_profile)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if not request.user.is_vendor():
            return redirect('home')
        
        vendor_profile = request.user.vendor_profile
        form = self.form_class(request.POST, instance=vendor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('vendor:dashboard')
        
        return render(request, self.template_name, {'form': form})


class VendorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = VendorProfile
    template_name = 'vendor/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(store_name__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        
        # Filter by approval status
        approval_filter = self.request.GET.get('is_approved', '')
        if approval_filter in ['true', 'false']:
            queryset = queryset.filter(is_approved=(approval_filter == 'true'))
        
        # Sorting
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


class VendorDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = VendorProfile
    template_name = 'vendor/vendor_detail.html'
    context_object_name = 'vendor'
    