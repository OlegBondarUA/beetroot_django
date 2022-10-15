from django.views.generic import FormView, TemplateView
from django.contrib import messages

from . forms import ContactForm
from . models import Contact


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        messages.add_message(
            self.request, messages.SUCCESS,
            f"Thank you {form.cleaned_data.get('name').upper()}, "
            "for your message!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING,
            'Please send correct data!'
        )
        return super().form_invalid(form)


class InfoView(TemplateView):
    template_name = 'element-counters.html'
