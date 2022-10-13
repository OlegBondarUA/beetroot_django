from django.urls import path

from . import views

urlpatterns = [
    path('contact-us/', views.ContactView.as_view(), name='contact'),
    path('info/', views.InfoView.as_view(), name='info'),
]
