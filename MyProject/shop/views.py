from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from .models import Product


class HomePageViews(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        return context


def search_result(request):

    if request.method == "POST":
        return render(request, 'shop/search_result.html', {})

    else:
        return render(request, 'shop/search_result.html', {})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product_detail'
    query_pk_and_slug = True
