from django.http import HttpResponseRedirect
from django.urls import reverse

from .selectors import categories_selector, random_products_selector
from website.forms import SubscribeForm


def categories_menu(request):
    return {
        'search_categories': categories_selector()
    }


def featured_products(request):
    return {
        'featured_products': random_products_selector()
    }


def get_subscribe_email(request):
    if request.method == 'GET':
        form = SubscribeForm(request.GET)
        if form.is_valid():
            print(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(request.path)
            # return HttpResponseRedirect(request.path)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscribeForm()
    return {
        'form_subscribe': form
    }
