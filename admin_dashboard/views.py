from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from vendor.models import VendorProfile
from product.models import Product, Category

def admin_check(user):
    return user.is_authenticated and user.is_admin()

@login_required
@user_passes_test(admin_check)
def dashboard(request):
    vendor_count = VendorProfile.objects.count()
    product_count = Product.objects.count()
    recent_vendors = VendorProfile.objects.select_related('user').order_by('-user__date_joined')[:5]
    
    context = {
        'vendor_count': vendor_count,
        'product_count': product_count,
        'recent_vendors': recent_vendors,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

# Add other admin views (vendor_list, product_list, etc.)