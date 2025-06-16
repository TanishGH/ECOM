from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('vendors/', views.vendor_list, name='vendor_list'),
    # path('products/', views.product_list, name='product_list'),
    # path('categories/', views.category_list, name='category_list'),
]