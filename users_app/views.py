from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import SignUpForm


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'users_app/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.patronymic = form.changed_data.get('patronymic')
            user.profile.birthday = form.changed_data.get('birthday')
            user.save()
            user = authenticate(username=user.username)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, 'users_app/signup.html', {'form': form})
