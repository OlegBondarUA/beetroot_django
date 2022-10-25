from django.contrib import messages
from django.shortcuts import reverse
from django.db.transaction import atomic

from website.forms import SubscribeForm
from website.models import Subscribe
from utils.email import send_html_email
from .selectors import categories_selector, random_products_selector


def categories_menu(request):
    return {
        'search_categories': categories_selector()
    }


def featured_products(request):
    return {
        'featured_products': random_products_selector()
    }


@atomic
def get_subscribe_email(request):
    if request.method == 'GET':
        form = SubscribeForm(request.GET)
        if form.data.get('email') and form.is_valid():
            email = form.cleaned_data.get('email')
            email, created = Subscribe.objects.get_or_create(email=email)
            if created:
                send_html_email(
                    subject='Welcome to our website',
                    to_emails=[email.email],
                    context={
                        'name': '',
                        'link': request.build_absolute_uri(reverse('index')),
                    },
                    template_name='emails/email.html'
                )
            messages.add_message(
                request, messages.SUCCESS,
                'Thank you for subscribe!'
            )
        elif form.data.get('email') and not form.is_valid():
            messages.add_message(
                request, messages.WARNING,
                'Please send correct data!'
            )
    else:
        form = SubscribeForm()
    return {
        'subscribe_form': form
    }
