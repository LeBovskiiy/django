from django.urls import path
from .views import HomePageViews, SearchResultView, ProductDetailView


urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('search/', SearchResultView.as_view(), name='search-result'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
#
# urlpatterns += [
#     path(r'^product/search/(?P<name>[-\w]+)/$', )
# ]