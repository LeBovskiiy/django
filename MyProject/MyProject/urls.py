from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.base_view import BaseView, MethodNotAllowedView


handler404 = BaseView.as_view()
handler403 = BaseView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('path/to/method-not-allowed/', MethodNotAllowedView.as_view(), name='method-not-allowed')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
