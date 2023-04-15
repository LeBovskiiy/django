from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, ListView, View
from .models import Product
from django.views.decorators.csrf import csrf_protect


from users.models import CartItem, Basket
from .models import Product

class BaseView(View):
    """Базовый класс для всех вюшек, который обрабатывает исключения."""
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as Ex:
            return self._responce({'errorMessage': Ex.message})
        
        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response
        


class HomePageViews(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:5]

        return context


class SearchResultView(ListView):
    model = Product
    template_name = 'shop/search_result.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product_detail'
    query_pk_and_slug = True


class BasketView(View):
    """This View created for work with User Basket"""
    def add_to_cart(self, product_id):
        if not self.user.is_anonymus():
            product = get_object_or_404(Product, id=product_id)
            if isinstance(self.user.id, int):
                basket, created = Basket.objects.get_or_create(handler=self.user)
                cart_item, created = CartItem.objects.get_or_create(basket=basket, product=product)
                cart_item.quantity += 1
                cart_item.save()
                return redirect('product-detail')
        elif self.user.id == None or not isinstance(self.user.id, int):
            return HttpResponse("<h1>Sorry, but you need to log-in if you want add product to basket</h1>")

    def remove_from_cart(self, product_id):
        product = Product.objects.get(id=product_id)
        basket = Basket.objects.get(handler=self.user)
        cart_item = CartItem.objects.get(basket=basket, product=product)
        if cart_item:
            cart_item.delete()
            return redirect('basket')
        else:
            return HttpResponse('<h1>Objects not Found</h1>')

    def view_cart(self):
        basket = Basket.objects.get(handler=self.user)
        cart_items = basket.baskets.all()
        return render(self, 'shop/basket.html', {'cart_items': cart_items})
    

    