
from django.contrib import admin
from .models import VendorProfile

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('store_name', 'user__username')