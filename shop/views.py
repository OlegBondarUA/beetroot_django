from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def catalogue(request):
    context = {}
    return render(request, 'category.html', context)


def product(request):
    context = {}
    return render(request, 'product.html', context)
