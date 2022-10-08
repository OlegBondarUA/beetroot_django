from random import sample

from django.db.models import F

from .models import Product


def random_products_selector(products_number: int = 4):
    project_ids = Product.objects.values_list('pk', flat=True)
    random_ids = sample(list(project_ids), products_number)
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).filter(pk__in=random_ids)


def new_arrivals_products_selector(products_limit: int = 5):
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-date_created')[:products_limit]


def best_price_products_selector(products_limit: int = 3):
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).filter(
        old_price__isnull=False
    ).annotate(
        best_price=F('old_price') - F('price')
    ).order_by('-best_price')[:products_limit]


def top_products_selector(products_limit: int = 3):
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-price')[:products_limit]
