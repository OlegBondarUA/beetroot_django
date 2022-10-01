from django.shortcuts import render, get_object_or_404

from . models import Category, Product


def index(request):
    categories = Category.objects.all()[:10]
    products = Product.objects.prefetch_related('images')[:4]
    context = {
        'categories': categories,
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
