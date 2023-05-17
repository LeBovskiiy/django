from typing import Any, Dict

import django.http as http
from django import http
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)
from rest_framework import generics

from users.models import Basket, CartItem

from .base_view import BaseView, MethodNotAllowedView
from .forms import *
from .models import *
from .serilizers import ProductSerializer


class HomePageViews(TemplateView, BaseView):
    template_name = 'shop/home.html'

    def http_method_not_allowed(self, request, *args, **kwargs) -> http.HttpResponse:
        return super().http_method_not_allowed(request, *args, **kwargs)
    
    def get(self, request: HttpRequest) -> HttpResponse:
        prodcuts = Product.objects.all()[:5]
        categories = ProductCategory.objects.all()
        context = {
            'products': prodcuts,
            'categories': categories
        }
        return render(request, 'shop/home.html', context)
    

class SearchResultView(ListView, BaseView):
    """Класс для работы с Сьорч-баром (из шаблона 'shop/navbar.html')"""

    model = Product
    template_name = 'shop/search_result.html'
    context_object_name = 'products'
    paginate_by = 10

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_queryset(self, *args, **kwargs):
        """Функцыя для работы с Сьорч-баром (из шаблона 'shop/navbar.html')"""
        query = self.request.GET.get('q')
        sort_q = self.request.GET.get('sort-by')
        search_query = self.request.session.get('search_query')

        if query and sort_q is None:
            """"Этот блок кода срабатывает, когда: пользователь ввьол запрос, но ещьо не фильтровал его под свои нужды( как правило, по идеи это самый первый запрос )"""
            self.request.session['search_query'] = query        # сюда я записую пользовательский запрос, что б использовать его для фильтрации
            response = Product.objects.filter(
                Q(name__istartswith=query)
            )
            return response
        
        elif search_query and sort_q:
            """Этот блок кода срабатывает когда пользователь рание делал запрос, и хочет его отфильтровать"""
            response = Product.objects.filter(name__istartswith=search_query).order_by(sort_q)
            return response

        elif sort_q  is None and query is None and search_query:
            """Этот блок кода срабатывает когда: пользователь ничего не ввьол в поисковик, но получив все товары, хочет их отфильтровать"""
            response = Product.objects.all().order_by(sort_q)
            return response

        elif search_query is None and query is None and sort_q is None:
            """Этот блок кода срабатывает когда: пользователь ничего не вводил в поисковик, и не хочет фильтровать полученые товары"""
            response = Product.objects.all().order_by('name')
            return response
        else:
            return Product.objects.all()
    

class ProductDetailView(DetailView, BaseView):
    """Вюха для просмотра деталей товара."""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product_detail'
    query_pk_and_slug = True

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['review_form'] = UserReviewForm()
        context['comments'] = UserReview.objects.all().order_by('pub_date')[:10]
        return context
    
    def post(self, request, *args, **kwargs):
        form = UserReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            user = self.request.user
            review.product = self.get_object()
            review.user = user
            review.save()
            review.reset()
        else:
            return render(request, 'shop/errors.html', {'message': 'Form is not valid'})
            

class BasketView(BaseView):
    """Просматриваем содержымое корзины"""
    def get(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            basket = Basket.objects.get(handler=request.user)
            cart_items = basket.baskets.all()
            return render(request, 'shop/basket.html', {'cart_items': cart_items.order_by('product_id')})
        else:
            context = {'message': 'Что б иметь корзину вам нужно пройти аутентификацыю'}
            return render(request, 'shop/errors.html', context)


class CartActionView(BasketView):
    """Забираем товар с корзины"""
        
    def get(self, request: http.HttpRequest, product_id, action: str):

        if request.user.is_authenticated:
            if action == 'add':
                product = get_object_or_404(Product, id=product_id)
                basket, created = Basket.objects.get_or_create(handler=request.user)
                cart_item, created = CartItem.objects.get_or_create(basket=basket, product=product)
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    return redirect('shop:basket')
                else:
                    return http.JsonResponse({'success': False})
                
            elif action == 'subtract':
                product = Product.objects.get(id=product_id)
                basket = Basket.objects.get(handler=request.user)
                cart_item = CartItem.objects.get(basket=basket, product=product)
                if cart_item:
                    if cart_item.quantity >= 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        return redirect('shop:basket')
                    else:
                        cart_item.delete()
                        return redirect('shop:basket')
                else:
                    return http.JsonResponse({'success': False})
                
            elif action == 'delete':
                product = Product.objects.get(id=product_id)
                basket = Basket.objects.get(handler=request.user)
                cart_item = CartItem.objects.get(basket=basket, product=product)
                if cart_item:
                    cart_item.delete()
                    return redirect('shop:basket')
                else:
                    return http.JsonResponse({'success': False})


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoriesView(ListView, HomePageViews):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            self.categoryies = ProductCategory.objects.all()
            self.category = ProductCategory.objects.get(category='For Everyone')
            self.prodcuts = Product.objects.filter(categories=self.category)
            context = {
                'categories': self.category,
                'products_catehory': self.prodcuts,
                'categories': self.categoryies[:10]
                       }
            return render(request, 'shop/categories.html', context)


class ProductCategoryView(ListView):

    def get(self, request: HttpRequest, category_name) -> HttpResponse:
        categorie = ProductCategory.objects.get(category=category_name)
        products = Product.objects.filter(categories=categorie)
        context = {
            'products': products
        }
        return render(request, 'shop/prodcuts_by_categories.html', context=context)


class UserReviewView(CreateView):
    model = UserReview
    form_class = UserReviewForm
    success_url = 'users/review_thanks.html'

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        return super(UserReview, self).form_valid(form)


class UsersCommentsView(ListView):
    model = UserReview
    queryset = UserReview.objects.all().order_by('pub_date')[:10]
    paginate_by = 15

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        comments = UserReview.objects.all().order_by('pub_date')
        context = {
            'comments': '1 2 3 4 5 6 7 8 9 10'}
        return render(request, 'shop/comments.html', context)
    