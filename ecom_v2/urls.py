from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('vendor/', include('vendor.urls')),
    path('check-role/', user_views.CheckUserRoleView.as_view(), name='check_user_role'),
    path('product/', include('product.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)