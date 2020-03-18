from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy

from allauth.account.views import PasswordSetView


# auth
def signup(request, key):
    raise Http404


def login(request, key):
    raise Http404


def logout(request, key):
    raise Http404


# email
def email(request):
    raise Http404


def email_verification_sent(request):
    raise Http404


def confirm_email(request, key):
    raise Http404


# password
def password_change(request):
    raise Http404


def password_reset(request):
    raise Http404


def password_reset_done(request):
    raise Http404


def password_reset_from_key(request, uidb36, key):
    raise Http404


def password_reset_from_key_done(request):
    raise Http404


def account_inactive(request):
    raise Http404


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context
