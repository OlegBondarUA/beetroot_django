from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import FormView, TemplateView, ListView
from django.contrib import messages
from django.urls import reverse

from shop.models import Color, Product, Size
from shop import selectors
from utils.email import send_html_email
from . forms import ContactForm
from . models import Contact


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        to_email = form.cleaned_data.get('email')
        send_html_email(
            subject='Welcome to our website',
            to_emails=[to_email],
            context={
                'name': form.cleaned_data.get('name'),
                'link': self.request.build_absolute_uri(reverse('index')),
            },
            template_name='emails/email.html'
        )
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
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = {}
        if self.search_category:
            _filter = {
                'categories__name': self.search_category
            }

        return Product.objects.prefetch_related(
            'images', 'categories'
        ).annotate(
            rank=self._create_search_rank()
        ).filter(
            rank__gte=0.3,
            **_filter
        ).order_by('-rank')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = self.get_queryset().values_list('id', flat=True)

        aggregated_price_data = selectors.aggregated_price_data()
        context |= {
            'search_query': self.search_query,
            'search_result_count': self.get_queryset().count(),
            'sizes': selectors.products_sizes_selector(product_ids),
            'colors': selectors.products_colors_selector(product_ids),
            'brands': selectors.products_brands_selector(product_ids),
            'max_price': aggregated_price_data['max_price'],
            'average_price': aggregated_price_data['avg_price'],
            'min_price': aggregated_price_data['min_price'],
        }
        return context

    def _create_search_rank(self) -> SearchRank:
        if self.request.LANGUAGE_CODE == 'en-us':
            vector = SearchVector('title', weight='A') \
                     + SearchVector('description', weight='B') \
                     + SearchVector('color__name', weight='A')

            query = SearchQuery(self.search_query)
            rank = SearchRank(
                vector,
                query,
            )
        else:
            vector = SearchVector('title_ua', weight='A') \
                     + SearchVector('description_ua', weight='B') \
                     + SearchVector('color__name_ua', weight='A')
            query = SearchQuery(self.search_query)
            rank = SearchRank(
                vector,
                query,
             )
        return rank
