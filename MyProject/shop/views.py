from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, ListView
from .models import Product
from django.contrib.auth.decorators import login_required

from users.models import CartItem, Basket
from .models import Product


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

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product_detail'
    query_pk_and_slug = True


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(handler=request.user)
    cart_item, created = CartItem.objects.get_or_create(basket=basket, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('basket')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.get(handler=request.user)
    cart_item = CartItem.objects.get(basket=basket, product=product)
    if cart_item:
        cart_item.delete()
        return redirect('basket')
    else:
        return HttpResponse('<h1>Objects not Found</h1>')


def view_cart(request):
    basket = Basket.objects.get(handler=request.user)
    cart_items = basket.baskets.all()
    return render(request, 'shop/basket.html', {'cart_items': cart_items})