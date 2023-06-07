from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from shop.base_view import BaseView, MethodNotAllowedView

handler404 = BaseView.as_view()
handler403 = BaseView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api-auth/', include('rest_framework.urls', namespace='API')),
]
urlpatterns += i18n_patterns(
    path('', include('shop.urls', namespace='shop')),
    path('users/', include('users.urls', namespace='users')),
    path('users/', include('django.contrib.auth.urls')),
    path('method-not-allowed/', MethodNotAllowedView.as_view(), name='method-not-allowed'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
