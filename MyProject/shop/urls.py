from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('search/', SearchResultView.as_view(), name='search-result'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_basket/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('clear_session_query/', ClearSearchQueryView.as_view(), name='clear-search-query'),
    path('js_res/', js_res, name='js_res'),

]
