from django.urls import path, re_path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path(
        r'^activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1, 13}-[0-9A-Za-z]{1, 20})/$',
        views.ActivateView.as_view(), name='activate'
    ),
]
