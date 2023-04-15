from django.urls import path
from .views import HomePageViews, SearchResultView, ProductDetailView, BasketView

urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('search/', SearchResultView.as_view(), name='search-result'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('basket/', BasketView.view_cart, name='basket'),
    path('add_to_cart/<int:product_id>/', BasketView.add_to_cart, name='add-to-cart'),
    path('remove_from_basket/<int:product_id>/', BasketView.remove_from_cart, name='remove-from-cart'),
    
]
