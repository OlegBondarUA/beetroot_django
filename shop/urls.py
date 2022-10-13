from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalogue/<slug:slug>/', views.CatalogueView.as_view(), name='catalogue'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),
]
