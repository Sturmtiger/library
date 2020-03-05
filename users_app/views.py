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

from .forms import (SignUpForm, CreatePublisherUserForm,
                    UpdateUserForm, UpdateProfileForm,
                    AssignPublisherCompanyToUserPublisherForm)
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
        create_publisher_form = CreatePublisherUserForm()
        assign_publisher_form = AssignPublisherCompanyToUserPublisherForm()

        context = {
            'create_publisher_form': create_publisher_form,
            'assign_publisher_form': assign_publisher_form
        }

        return render(request, 'users_app/admin_panel.html', context=context)

    def post(self, request):
        create_publisher_form = CreatePublisherUserForm()
        assign_publisher_form = AssignPublisherCompanyToUserPublisherForm()

        if 'invite_publisher' in request.POST:
            create_publisher_form = CreatePublisherUserForm(request.POST)
            if create_publisher_form.is_valid():
                user = create_publisher_form.save()

                # Send email to publisher-user to set password
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain

                mail_context = {
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if self.request.is_secure()
                                else 'http',
                }

                subject = render_to_string(
                    'users_app/password_set/subject.txt')
                message = render_to_string(
                    'users_app/password_set/email.html',
                    context=mail_context)

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[user.email],
                )
                messages.success(request,
                                 'Publisher-user has been created '
                                 'and message has been sent.')

        if 'assign_company' in request.POST:
            assign_publisher_form = AssignPublisherCompanyToUserPublisherForm(
                request.POST)
            if assign_publisher_form.is_valid():
                publisher_user = assign_publisher_form.save()
                publisher_company = publisher_user.profile.publisher_company
                messages.success(request,
                                 f'Publisher-company "{publisher_company}" '
                                 f'has been assigned to "{publisher_user}".')

        context = {
            'create_publisher_form': create_publisher_form,
            'assign_publisher_form': assign_publisher_form
        }

        return render(request, 'users_app/admin_panel.html', context=context)


class UserProfileView(View):
    def get(self, request):
        return render(request, 'users_app/profile.html')


class UpdateUserView(View):
    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        next_url = self.request.GET.get('next', '/')
        return render(request, 'users_app/update_user.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'next': next_url,
        })

    @transaction.atomic
    def post(self, request):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         instance=request.user.profile)
        next_url = self.request.GET.get('next', '/')

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,
                             'Your data has been updated successfully!')
            return redirect(next_url)
        return render(request, 'users_app/update_user.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'next': next_url,
        })
