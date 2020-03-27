from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import (DetailView, FormView, TemplateView,
                                  UpdateView, CreateView)

from .celery_tasks import send_mail_async
from .custom_mixins import (AnonymousUserRequired, UserIsAdmin,
                            CurrentUserObjectMixin)
from .forms import (AssignPublisherCompanyToUserPublisherForm,
                    CreatePublisherUserForm, SignUpForm, UpdateProfileForm,
                    UpdateUserForm)
from .models import Profile


class SignUpView(AnonymousUserRequired, CreateView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = settings.LOGIN_REDIRECT_URL

    @transaction.atomic
    def form_valid(self, form):
        # new user obj
        self.object = form.save()
        self.object.refresh_from_db()
        self.object.profile.patronymic = form.cleaned_data.get("patronymic")
        self.object.profile.birthday = form.cleaned_data.get("birthday")
        self.object.profile.get_newsletter = form.cleaned_data.get("get_newsletter")
        self.object.profile.type = Profile.READER
        self.object.save()

        password = form.cleaned_data.get("password1")
        user = authenticate(username=self.object.username, password=password)
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(CurrentUserObjectMixin, UpdateView):
    form_class = UpdateUserForm
    second_form_class = UpdateProfileForm
    template_name = "users/update_user.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()

        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context["user_form"] = self.form_class(instance=user)
        if "profile_form" not in context:
            context["profile_form"] = self.second_form_class(instance=user.profile)
        context["next"] = self.request.GET.get("next", "/")
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.get_object()

        user_form = self.form_class(request.POST, instance=user)
        profile_form = self.second_form_class(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your data has been updated successfully!")
            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(user_form=user_form, profile_form=profile_form)
        )

    def get_success_url(self):
        next_url = self.request.GET.get("next", "/")
        return next_url


class AdminPanelView(UserIsAdmin, TemplateView):
    template_name = "users/admin_panel.html"


class AssignPublisherCompanyToUserPublisherView(UserIsAdmin, FormView):
    template_name = "users/assign_publisher_company_to_user_publisher.html"
    form_class = AssignPublisherCompanyToUserPublisherForm

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            f'Publisher-company "{self.object.profile.publisher_company}" '
            f'has been assigned to "{self.object}".',
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "/")
        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", "/")
        return next_url


class CreatePublisherUserView(UserIsAdmin, CreateView):
    template_name = "users/create_user_publisher.html"
    form_class = CreatePublisherUserForm

    def form_valid(self, form):
        # created user obj
        self.object = form.save()

        # Send email to publisher-user to set password
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain

        mail_context = {
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(self.object.pk)),
            "user": self.object,
            "token": default_token_generator.make_token(self.object),
            "protocol": "https" if self.request.is_secure() else "http",
        }

        subject = render_to_string("users/password_set/subject.txt")
        message = render_to_string(
            "users/password_set/email.html", context=mail_context
        )

        send_mail_async.delay(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[self.object.email],
        )

        messages.success(
            self.request,
            "User-publisher has been created and message has been sent.",
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "/")
        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next", "/")
        return next_url


class UserProfileView(LoginRequiredMixin, CurrentUserObjectMixin, DetailView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        books = None
        if (user.profile.type == Profile.PUBLISHER
                and user.profile.publisher_company):
            books = user.profile.publisher_company.books.all()

        context = super().get_context_data(**kwargs)
        context["books"] = books
        return context


class CustomPasswordResetView(AnonymousUserRequired, PasswordResetView):
    template_name = "users/password_reset/form.html"
    subject_template_name = "users/password_reset/subject.txt"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset/confirm.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().dispatch(*args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "/")
        return context
