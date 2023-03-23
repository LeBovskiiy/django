from django.urls import path
from .views import HomePageViews, search_result, ProductDetailView


urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('search/', search_result, name='search-result'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]