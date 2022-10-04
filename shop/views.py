from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from . models import Category, Product


def index(request):
    search_categories = Category.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gte=5
    ).order_by('-products_count')

    products = Product.objects.prefetch_related('images', 'categories')[:4]

    context = {
        'categories': search_categories[:10],
        'search_categories': search_categories,
        'featured_products': products,
    }

    return render(request, 'index.html', context)


def catalogue(request):
    context = {}
    return render(request, 'category.html', context)


def product(request, **kwargs):
    item = get_object_or_404(Product, slug=kwargs.get('slug'))
    context = {
        'product': item
    }
    return render(request, 'product.html', context)
