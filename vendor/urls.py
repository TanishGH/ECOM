from django.urls import path
from .views import (
    VendorDashboardView,
    CompleteProfileView,
    EditProfileView,
    VendorListView,
    VendorDetailView
)

app_name = 'vendor'

urlpatterns = [
    path('dashboard/', VendorDashboardView.as_view(), name='dashboard'),
    path('profile/complete/', CompleteProfileView.as_view(), name='complete_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    
    
    
]