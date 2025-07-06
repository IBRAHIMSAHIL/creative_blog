from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from adminpanel import views as admin_views  # For direct dashboard routing

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth & User-related URLs
    path('users/', include('users.urls')),

    # Blog (main app)
    path('', include('blog.urls')),

    # Admin Dashboard (choose ONE of the two options below ⬇)

    # Option 1: ✅ If you only have one dashboard view:
    path('admin-dashboard/', admin_views.dashboard, name='admin_dashboard'),

    # Option 2: ❌ [Skip this unless you're using multiple admin views]
    # path('admin-dashboard/', include('adminpanel.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
