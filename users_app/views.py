from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.db import transaction

from .forms import SignUpForm, CreatePublisherUserForm
from .models import Profile
from .custom_mixins import UserIsAdminMixin


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'users_app/signup.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(request.POST)
            user = form.save()
            user.refresh_from_db()
            user.profile.patronymic = form.cleaned_data.get('patronymic')
            user.profile.birthday = form.cleaned_data.get('birthday')
            user.profile.type = Profile.READER
            user.save()

            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, 'users_app/signup.html', {'form': form})


class AdminPanelView(UserIsAdminMixin, View):
    def get(self, request):
        form = CreatePublisherUserForm()
        return render(request, 'users_app/admin_panel.html', {'form': form})

    def post(self, request):
        form = CreatePublisherUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send email to publisher-user to set password
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain

            context = {
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }

            subject = render_to_string('users_app/password_set/subject.txt')
            message = render_to_string(
                'users_app/password_set/email.html',
                context=context
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
            )
            messages.success(request, 'Publisher-user has been created.')

        return render(request, 'users_app/admin_panel.html', {'form': form})
