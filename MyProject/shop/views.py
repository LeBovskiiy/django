import django.http as http
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, ListView, View
from django.views.decorators.csrf import csrf_protect

from .base_view import BaseView
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
        if query != '' and sort_q is None:
            self.request.session['search_query'] = query
            response = Product.objects.filter(
                Q(name__icontains=query)
            )
            return response
        elif self.request.session.get('search_query') != None and sort_q:
            response = Product.objects.filter(name__icontains=self.request.session.get('search_query')).order_by(sort_q)
            return response

        elif self.request.session.get('search_query') is None and query is None and sort_q is not None:
            response = Product.objects.all().order_by(sort_q)
            return response

        elif self.request.session.get('search_query') is None and query is None and sort_q is None:
            response = Product.objects.all()
            return response

        elif query == '':
            response = Product.objects.all()
            return response
        
class ClearSearchQueryView(View):
    def get(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            basket = Basket.objects.get(handler=request.user)
            cart_items = basket.baskets.all()
            return render(self, 'shop/basket.html', {'cart_items': cart_items})
        else:
            context = {'message': 'Что б иметь корзину вам нужно пройти аутентификацыю'}
            return render(self, 'shop/errors.html', context)


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
            return render(request, 'shop/basket.html', {'cart_items': cart_items})
        else:
            context = {'message': 'Что б иметь корзину вам нужно пройти аутентификацыю'}
            return render(request, 'shop/errors.html', context)


class AddToCartView(BasketView):
    """Добавляем товар к корзине"""
    def get(self, request, product_id):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            if isinstance(request.user.id, int):
                basket, created = Basket.objects.get_or_create(handler=request.user)
                cart_item, created = CartItem.objects.get_or_create(basket=basket, product=product)
                cart_item.quantity += 1
                cart_item.save()
                return redirect('product-detail', pk=product_id)
        else:
            context = {'message': 'Что б добавлять товары в корзину, \
                        ван нужно пройти аутентификаыю'}
            return render(self, 'shop/errors.html', context)


class RemoveFromCartView(BasketView):
    """Забираем товар с корзины"""
    def get(self, request: http.HttpRequest, product_id):
        if request.user.is_authenticated:
            product = Product.objects.get(id=product_id)
            basket = Basket.objects.get(handler=request.user)
            cart_item = CartItem.objects.get(basket=basket, product=product)
            if cart_item:
                cart_item.delete()
                return redirect('basket')
            else:
                return http.HttpResponse('<h1>Objects not Found</h1>')
        else:
            context = {'message': 'Что б что-то удалять с корзины, вы должны иметь корзину'}
            return render(request, 'shop/errors.html', context)

    
def js_res(request):
    return http.JsonResponse({'success': True})


 
    

    