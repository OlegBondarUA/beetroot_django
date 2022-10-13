from django.views.generic import TemplateView, DetailView, ListView

from . models import Product, Size, Color
from . import selectors


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'new_arrivals': selectors.new_arrivals_products_selector(),
            'best_price': selectors.best_price_products_selector(),
            'top_products': selectors.top_products_selector(),
        }
        return context


class CatalogueView(ListView):
    template_name = 'category.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        if page_by := self.request.GET.get('count'):
            self.paginate_by = page_by
        self.size = Size.objects.get(name=self.request.GET['size']) \
            if self.request.GET.get('size') else None
        self.color = Color.objects.get(name=self.request.GET['color']) \
            if self.request.GET.get('color') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = {
            'categories__slug': self.kwargs.get('slug')
        }
        if self.size:
            _filter['sizes__name'] = self.size.name
        if self.color:
            _filter['color__name'] = self.color.name

        return Product.objects.prefetch_related(
            'images', 'categories'
        ).filter(**_filter).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = self.get_queryset().values_list('id', flat=True)

        aggregated_price_data = selectors.aggregated_price_data()
        context |= {
            'sizes': selectors.products_sizes_selector(product_ids),
            'colors': selectors.products_colors_selector(product_ids),
            'brands': selectors.products_brands_selector(product_ids),
            'max_price': aggregated_price_data['max_price'],
            'average_price': aggregated_price_data['avg_price'],
            'min_price': aggregated_price_data['min_price'],
        }
        return context


class ProductView(DetailView):
    template_name = 'product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.prefetch_related('images', 'categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'new_arrivals': selectors.new_arrivals_products_selector(),
            'best_price': selectors.best_price_products_selector(),
            'top_products': selectors.top_products_selector(),
            'related_products': selectors.related_products_selector(self.object),
        }
        return context
