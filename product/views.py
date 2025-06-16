from django.views.generic import (
    ListView, CreateView, UpdateView, 
    DeleteView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from vendor.models import VendorProfile

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        vendor = self.request.user.vendor_profile
        queryset = super().get_queryset().filter(vendor=vendor).annotate(
            product_count=Count('products')
        )
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Sorting
        sort = self.request.GET.get('sort', '')
        sort_options = {
            'name_asc': 'name',
            'name_desc': '-name',
            'count_asc': 'product_count',
            'count_desc': '-product_count',
            'date_asc': 'created_at',
            'date_desc': '-created_at',
        }
        if sort in sort_options:
            queryset = queryset.order_by(sort_options[sort])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'product/category_form.html'
    success_url = reverse_lazy('product:category_list')

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor_profile
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'product/category_form.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product:category_list')

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user.vendor_profile)

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'product/category_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product:category_list')

    def get_queryset(self):
        return super().get_queryset().filter(vendor=self.request.user.vendor_profile)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        vendor = self.request.user.vendor_profile
        queryset = super().get_queryset().filter(
            category__vendor=vendor
        ).select_related('category')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Category filter
        category_filter = self.request.GET.get('category', '')
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        
        # Tag filter
        tag_filter = self.request.GET.get('tag', '')
        if tag_filter:
            queryset = queryset.filter(tags__icontains=tag_filter)
        
        # Sorting
        sort = self.request.GET.get('sort', '')
        sort_options = {
            'name_asc': 'name',
            'name_desc': '-name',
            'price_asc': 'price',
            'price_desc': '-price',
            'stock_asc': 'stock',
            'stock_desc': '-stock',
            'date_asc': 'created_at',
            'date_desc': '-created_at',
        }
        if sort in sort_options:
            queryset = queryset.order_by(sort_options[sort])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.request.user.vendor_profile
        
        # Get all categories for filter dropdown
        context['categories'] = Category.objects.filter(
            vendor=vendor
        ).only('id', 'name')
        
        # Extract unique tags for filter dropdown
        tags = set()
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        
        if not (search_query or category_filter):
            tags = set(Product.objects
                      .filter(category__vendor=vendor)
                      .exclude(tags__exact='')
                      .values_list('tags', flat=True))
            tags = {tag.strip() for tag_list in tags for tag in tag_list.split(',') if tag.strip()}
        else:
            for product in self.get_queryset():
                if product.tags:
                    tags.update(tag.strip() for tag in product.tags.split(',') if tag.strip())
        
        context.update({
            'tags': sorted(tags),
            'search_query': search_query,
            'selected_category': category_filter,
            'selected_tag': self.request.GET.get('tag', ''),
            'selected_sort': self.request.GET.get('sort', ''),
        })
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product:product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.request.user.vendor_profile
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product:product_list')

    def get_queryset(self):
        return super().get_queryset().filter(
            category__vendor=self.request.user.vendor_profile
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.request.user.vendor_profile
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product:product_list')

    def get_queryset(self):
        return super().get_queryset().filter(
            category__vendor=self.request.user.vendor_profile
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(
            category__vendor=self.request.user.vendor_profile
        )