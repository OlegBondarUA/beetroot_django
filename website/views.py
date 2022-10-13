from django.views.generic import FormView, TemplateView

from . forms import ContactForm
from . models import Contact


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class InfoView(TemplateView):
    template_name = 'element-counters.html'
