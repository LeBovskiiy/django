import django.http as http
from django import http
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics

from users.models import CartItem

from .base_view import BaseView
from .forms import UserReview, UserReviewForm
from .models import Product, ProductCategory
from .serilizers import ProductSerializer, \
                        ProductCategorySerializer, \
                        ProductByCategorySerializer 


class HomePageViews(TemplateView, BaseView):
    '''Вюха домашней страницы'''
    template_name = 'shop/home.html'

    def http_method_not_allowed(self, request, *args, **kwargs) -> http.HttpResponse:
        return super().http_method_not_allowed(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.on_home()[:5]
        context['categories'] = ProductCategory.objects.get_all_categories()[:10]
        return context     

class SearchResultView(ListView, BaseView):
    '''Класс для работы с Сьорч-баром (из шаблона 'shop/navbar.html')'''
    model = Product
    template_name = 'shop/search_result.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)
        
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        sort_q = self.request.GET.get('sort-by')
        search_query = self.request.session.get('search_query')

        if query and sort_q is None:
            self.request.session['search_query'] = query
            response = Product.objects.filter_by_name(query)
            return response
        
        elif search_query and sort_q:
            response = Product.objects.filter_by_name(search_query).order_by(sort_q)
            return response

        elif sort_q  is None and query is None and search_query:
            # TODO: Нужно заблокировать сьорч бар, что б пустой запрос не мог вызваться
            response = Product.objects.all().order_by(sort_q)
            return response

        elif search_query is None and query is None and sort_q is None:
            response = Product.objects.all().order_by('name')
            return response
        else:
            return Product.objects.all()
    

class BasketView(BaseView, LoginRequiredMixin):
    '''Просматриваем содержымое корзины'''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItem.objects.get_items(user=self.request.user)
        return context
    
    def get(self, request: http.HttpRequest, *args, **kwargs):
        cart_items = CartItem.objects.get_items(request.user)
        context = {'cart_items': cart_items}
        return render(request, 'shop/basket.html', context)
        

class CartActionView(BasketView, LoginRequiredMixin):
    '''Забираем товар с корзины'''
            
    def get(self, request, product_id, action):
        user = request.user
        if action == 'add':
            response = CartItem.objects.add_quantity(product_id, user=user)
            if response:
                return redirect('shop:basket')
            else:
                return http.JsonResponse({'success': False})
        if action == 'subtract':
            response = CartItem.objects.subtract_quantity(product_id=product_id, user=user)
            if response:
                return redirect('shop:basket')
            else:
                return http.JsonResponse({'success': False})
            
        if action == 'delete':
            response = CartItem.objects.delete_cart_item(product_id, user)
            if response:
                return redirect('shop:basket')
            else:
                return http.JsonResponse({'success': False})


class CategoriesView(ListView, HomePageViews):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            self.categoryies = ProductCategory.objects.get_all_categories()[:10]
            context = {
                'categories': self.categoryies
                       }
            return render(request, 'shop/categories.html', context)


class ProductCategoryView(BaseView, ListView):

    def get(self, request: HttpRequest, cate_id) -> HttpResponse:
        products = ProductCategory.objects.get_products_by_category(cate_id)
        context = {
            'products': products
        }
        return render(request, 'shop/prodcuts_by_categories.html', context=context) 


class UserReviewView(BaseView, CreateView, LoginRequiredMixin):
    model = UserReview
    form_class = UserReviewForm
    success_url = 'users/review_thanks.html'

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        return super(UserReview, self).form_valid(form)


class UsersCommentsView(BaseView, ListView):
    template_name = 'shop/comments.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.kwargs)
        context['comments'] = self.get_queryset()
        return context
    
    def get_queryset(self, **kwargs):
        product_id = self.kwargs['product_id']
        comments = Product.objects.get(id=product_id).comments.all()
        
        return comments


class ProductDetailView(BaseView, DetailView):
    '''Вюха для просмотра деталей товара'''
    model = Product
    template_name = 'shop/product_detail.html'
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UserReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            user = self.request.user
            review.product = self.get_object()
            review.user = user
            review.save()
        else:
            return render(request, 'shop/errors.html', {
                'message': 'Form is not valid'
                })
        return render(request, 'shop/product_detail.html', context=context)    
            
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['pk'])
        context['product'] = product
        context['review_form'] = UserReviewForm()
        context['comments'] = product.comments.all()      
        return context
    
    
class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class ProductCategoryAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    
class ProductByCategoryAPIView(generics.ListAPIView):
    serializer_class = ProductByCategorySerializer
    
    def get_queryset(self):
        category_name = self.kwargs['category']
        return ProductCategory.objects \
                .get_products_by_category(category_name) \
                .prefetch_related('product') \
                .values('name', 'description','price')
    