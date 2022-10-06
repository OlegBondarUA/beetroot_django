from random import randint

from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from . models import Category, Product, Size


def index(request):
    search_categories = Category.objects.prefetch_related(
        'products'
    ).annotate(
        products_count=Count('products')
    ).filter(
        products_count__gte=5
    ).order_by('-products_count')

    projects_count = Product.objects.count()
    min_index = randint(0, Product.objects.count())
    min_index = min_index if min_index < projects_count - 4 else min_index - 4
    max_index = min_index + 4
    products = Product.objects.prefetch_related(
        'images', 'categories'
    )[min_index: max_index]

    new_arrivals = Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-date_created')[:5]

    context = {
        'categories': search_categories[:10],
        'search_categories': search_categories,
        'featured_products': products,
        'new_arrivals': new_arrivals
    }

    return render(request, 'index.html', context)


def catalogue(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.filter(categories=category)[:12]
    sizes = Size.objects.filter(
        products__in=products
    ).distinct().order_by('name')

    context = {
        'products': products,
        'sizes': sizes,
    }
    return render(request, 'category.html', context)


def product(request, **kwargs):
    item = get_object_or_404(Product, slug=kwargs.get('slug'))
    context = {
        'product': item
    }
    return render(request, 'product.html', context)
