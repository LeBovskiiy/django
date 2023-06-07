from django.urls import path

from .views import HomePageViews, SearchResultView, \
                   ProductDetailView, UserReviewView, \
                   BasketView, ProductCategoryAPIView, \
                   CartActionView, ProductCategoryView, \
                   ProductAPIView, ProductByCategoryAPIView \
                   
                   

app_name = 'shop'

urlpatterns = [
    path(
        '', 
        HomePageViews.as_view(), 
        name='home'
        ),
    path(
        'search/', 
        SearchResultView.as_view(), 
        name='search-result'
        ),
    path(
        'product/<int:pk>/', 
        ProductDetailView.as_view(), 
        name='product-detail'
        ),
    path(
        'product/<int:pk>/review/', 
        UserReviewView.as_view(), 
        name='user_review'
        ),
    path(
        'basket/', 
        BasketView.as_view(), 
        name='basket'
        ),
    path(
        'cart_action/<int:product_id>/<str:action>/',
        CartActionView.as_view(), 
        name='cart-action'
        ),
    path(
        'prodcuts_by_categories/<str:cate_id>/',
        ProductCategoryView.as_view(), 
        name='categorie'
        ),
    path(
        'api/v1/prodcucts/', 
        ProductAPIView.as_view(), 
        name='api-products'
        ),
    path(
        'api/v1/gategories/', 
        ProductCategoryAPIView.as_view(), 
        name='api-categories'
        ),
    path(
        'api/v1/product_by_category/<str:category>/', 
        ProductByCategoryAPIView.as_view(), 
        name='api-product-by-category'
        ),
]
