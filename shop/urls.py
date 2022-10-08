from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/<slug:slug>/', views.catalogue, name='catalogue'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('contact-us/', views.contact, name='contact'),
    path('info/', views.info_page, name='info'),
]
