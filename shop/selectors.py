from random import sample

from django.db.models import Count, F, QuerySet, Avg, Max, Min

from .models import Brand, Color, Category, Product, Size


def random_products_selector(products_number: int = 4) -> QuerySet[Product]:
    project_ids = Product.objects.values_list('pk', flat=True)
    random_ids = sample(list(project_ids), products_number)
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).exclude(
        images__image__isnull=False, images__image=''
    ).filter(pk__in=random_ids)


def new_arrivals_products_selector(products_limit: int = 5) -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-date_created')[:products_limit]


def best_price_products_selector(products_limit: int = 3) -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).filter(
        old_price__isnull=False
    ).annotate(
        best_price=F('old_price') - F('price')
    ).order_by('-best_price')[:products_limit]


def top_products_selector(products_limit: int = 3) -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        'images', 'categories'
    ).order_by('-price')[:products_limit]


def categories_selector() -> QuerySet[Category]:
    return Category.objects.prefetch_related(
        'products'
    ).annotate(
        products_count=Count('products')
    ).order_by('-products_count')


def aggregated_price_data() -> dict[str, str]:
    return Product.objects.aggregate(
        max_price=Max('price'),
        avg_price=Avg('price'),
        min_price=Min('price'),
    )


def products_sizes_selector(product_ids: list[int]) -> QuerySet[Size]:
    return Size.objects.filter(
        products__id__in=product_ids
    ).distinct().order_by('name')


def products_colors_selector(product_ids: list[int]) -> QuerySet[Color]:
    return Color.objects.filter(
        products__id__in=product_ids
    ).distinct().order_by('name')


def products_brands_selector(product_ids: list[int]) -> QuerySet[Color]:
    return Brand.objects.filter(
        products__id__in=product_ids
    ).distinct().order_by('name')


def related_products_selector(product: Product) -> QuerySet[Product]:
    return Product.objects.filter(categories__in=product.categories.all())[:4]
