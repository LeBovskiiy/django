from django.urls import path
from .views import HomePageViews, SearchResultView, ProductDetailView, add_to_cart, view_cart, remove_from_cart


urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('search/', SearchResultView.as_view(), name='search-result'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('basket/', view_cart, name='basket'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove_from_basket/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
]
