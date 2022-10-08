from random import sample

from django.db.models import Avg, Max, Min
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from . models import Category, Product, Size
from . import selectors


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'featured_products': selectors.random_products_selector(),
            'new_arrivals': selectors.new_arrivals_products_selector(),
            'best_price': selectors.best_price_products_selector(),
            'top_products': selectors.top_products_selector(),
        }
        return context


def catalogue(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.prefetch_related(
        'images', 'categories',
    ).filter(categories=category)[:12]

    sizes = Size.objects.filter(
        products__in=products
    ).distinct().order_by('name')

    aggregated_price_data = Product.objects.aggregate(
        max_price=Max('price'),
        avg_price=Avg('price'),
        min_price=Min('price'),
    )

    context = {
        'products': products,
        'sizes': sizes,
        'max_price': aggregated_price_data['max_price'],
        'average_price': aggregated_price_data['avg_price'],
        'min_price': aggregated_price_data['min_price'],
    }
    return render(request, 'category.html', context)


def product(request, **kwargs):
    item = get_object_or_404(
        Product.objects.prefetch_related('images', 'categories'),
        slug=kwargs.get('slug')
    )

    related_products = Product.objects.filter(
        categories__id__in=item.categories.all()
    ).values_list('id', flat=True)
    random_ids = sample(list(related_products), 4)
    related_products = Product.objects.prefetch_related(
        'images', 'categories'
    ).filter(pk__in=random_ids)

    context = {
        'product': item,
        'related_products': related_products,
    }
    return render(request, 'product.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def info_page(request):
    context = {}
    return render(request, 'element-counters.html', context)
