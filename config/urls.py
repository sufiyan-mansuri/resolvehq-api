from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('resolvehq-admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('resolvehq/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('resolvehq/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
