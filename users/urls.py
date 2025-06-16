from django.urls import path
from .views import (
    ResendVerificationView, UserLoginView, UserSignupView, CheckUserRoleView,
    AdminDashboardView, VendorListView, VendorDetailView,
    ApproveVendorView, ProductListView, ProductDetailView,
    CategoryListView, CategoryDetailView, ProfileView, EditProfileView, VerificationRequiredView, VerificationSentView, VerifyEmailView
)
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('check-role/', CheckUserRoleView.as_view(), name='check_user_role'),
    
    path('verification-sent/', VerificationSentView.as_view(), name='verification_sent'),
    path('verification-required/', VerificationRequiredView.as_view(), name='verification_required'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend_verification'),
    
    # Admin views
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('vendors/<int:pk>/approve/', ApproveVendorView.as_view(), name='approve_vendor'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # Profile views
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    
]