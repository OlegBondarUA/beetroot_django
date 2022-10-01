from django.urls import path

from . views import index, catalogue, product

urlpatterns = [
    path('', index, name='index'),
    path('catalogue/<slug:slug>/', catalogue, name='catalogue'),
    path('product/<slug:slug>/', product, name='product'),
]
