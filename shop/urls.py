from django.urls import path

from . views import index, catalogue, product

urlpatterns = [
    path('', index, name='index'),
    path('catalogue/', catalogue, name='catalogue'),
    path('product/', product, name='product'),
]
