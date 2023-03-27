from django.db.models import Q
from django.views.generic import TemplateView, DetailView, ListView
from .models import Product
from .forms import SearchProductForm


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
