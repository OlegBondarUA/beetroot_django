from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('catalogue/', views.catalogue, name='full_catalogue'),
    path('catalogue/<slug:slug>/', views.CatalogueView.as_view(), name='catalogue'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),
    path('contact-us/', views.ContactView.as_view(), name='contact'),
    path('info/', views.InfoView.as_view(), name='info'),
]
