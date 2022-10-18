from django.views.generic import FormView, TemplateView, ListView
from django.contrib import messages

from shop.models import Color, Product, Size
from shop import selectors
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


class SearchView(ListView):
    template_name = 'category.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12
    search_query = None
    search_category = None

    def get(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('q')
        self.search_category = self.request.GET.get('cat')
        if page_by := self.request.GET.get('count'):
            self.paginate_by = page_by
        self.size = Size.objects.get(name=self.request.GET['size']) \
            if self.request.GET.get('size') else None
        self.color = Color.objects.get(name=self.request.GET['color']) \
            if self.request.GET.get('color') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.LANGUAGE_CODE == 'en-us':
            _filter = {
                'title__icontains': self.search_query
            }
        else:
            _filter = {
                'title_ua__icontains': self.search_query
            }

        if self.size:
            _filter['sizes__name'] = self.size.name
        if self.color:
            _filter['color__name'] = self.color.name

        return Product.objects.prefetch_related(
            'images', 'categories'
        ).filter(**_filter).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = self.get_queryset().values_list('id', flat=True)

        aggregated_price_data = selectors.aggregated_price_data()
        context |= {
            'sizes': selectors.products_sizes_selector(product_ids),
            'colors': selectors.products_colors_selector(product_ids),
            'brands': selectors.products_brands_selector(product_ids),
            'max_price': aggregated_price_data['max_price'],
            'average_price': aggregated_price_data['avg_price'],
            'min_price': aggregated_price_data['min_price'],
        }
        return context
