from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, 
    CategoryDeleteView, ProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, ProductDetailView
)

app_name = 'product'

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Product URLs
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_create'),
    path('products/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]