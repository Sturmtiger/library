from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.db import transaction
from .forms import SignUpForm
from .models import Profile


class SignUp(View):
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


class AdminPanel(UserPassesTestMixin, View):
    def get(self, request):
        return HttpResponse('Good job')

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.profile.type == Profile.ADMIN
