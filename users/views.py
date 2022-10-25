import logging

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from . tokens import account_activation_token
from utils.email import send_html_email
from . forms import SignUpForm


User = get_user_model()

logger = logging.getLogger('logit')


class SignUpView(FormView):
    template_name = 'signup.html'
    model = User
    form_class = SignUpForm
    success_url = '/signup/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_html_email(
            subject='Please activate your account',
            context={
                'domain': get_current_site(self.request),
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            },
            template_name='emails/account_activation_email.html',
            to_emails=[user.email]
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING,
            f'Please send correct data! {form.error_messages}'
        )
        logger.error(form.error_messages)
        return super().form_invalid(form)


class ActivateView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uid')))
            user = User.objects.get(pk=uid)
        except Exception as error:
            logger.error(error)
            user = None

        if user is not None \
                and account_activation_token.check_token(
                user, kwargs.get('token')
        ):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(self.request, user)
            return redirect('index')
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'login.html'
    model = User
    form_class = AuthenticationForm
    success_url = '/login/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('index')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING,
            f'Please input correct data! {form.error_messages}'
        )
        logger.error(form.error_messages)
        return super().form_invalid(form)
