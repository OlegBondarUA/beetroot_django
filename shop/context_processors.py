from django.db.models import Count

from .models import Category


def categories_menu(request):
    categories = Category.objects.prefetch_related(
        'products'
    ).annotate(
        products_count=Count('products')
    ).order_by('-products_count')
    return {
        'search_categories': categories
    }
