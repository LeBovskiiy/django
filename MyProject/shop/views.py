import django.http as http
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q, QuerySet
from django.views.generic import TemplateView, DetailView, ListView, View

from .base_view import BaseView, MethodNotAllowedView
from users.models import CartItem, Basket
from .models import Product


class HomePageViews(TemplateView, BaseView):
    template_name = 'shop/home.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:5]

        return context
    def http_method_not_allowed(self, request, *args, **kwargs) -> http.HttpResponse:
        return super().http_method_not_allowed(request, *args, **kwargs)


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
    

class ClearSearchQueryView(View):

    def post(self, request: http.HttpRequest, *args, **kwargs):
        if request.session.get('search_query'):
            request.session.pop('search_query')
            return http.JsonResponse({'success': True})
        else:
            return http.JsonResponse({'success': False})


class ProductDetailView(DetailView, BaseView):
    """Вюха для просмотра деталей товара."""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product_detail'
    query_pk_and_slug = True

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


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
                    return redirect('basket')
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
                        return redirect('basket')
                    else:
                        cart_item.delete()
                        return redirect('basket')
                else:
                    return http.JsonResponse({'success': False})
                
            elif action == 'delete':
                product = Product.objects.get(id=product_id)
                basket = Basket.objects.get(handler=request.user)
                cart_item = CartItem.objects.get(basket=basket, product=product)
                if cart_item:
                    cart_item.delete()
                    return redirect('basket')
                else:
                    return http.JsonResponse({'success': False})
                
                
            



        
def js_res(request):
    return http.JsonResponse({'success': True})