from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Profile
from library_app.models import PublisherCompany
from .utils import gen_username_from_email


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    birthday = forms.DateField(help_text='Format: YYYY-MM-DD',
                               required=False)
    patronymic = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic',
                  'email', 'birthday', 'password1', 'password2',)


class CreatePublisherUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('email',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        username = gen_username_from_email(self.cleaned_data['email'])

        user.username = username
        user.set_unusable_password()
        if commit:
            user.save()
            user.refresh_from_db()
            user.profile.type = Profile.PUBLISHER
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email


class UpdateUserForm(forms.ModelForm):
    class Meta:
        fields = ('username', 'last_name', 'first_name',)
        model = User


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ('patronymic', 'birthday',)
        model = Profile


class AssignPublisherCompanyToUserPublisherForm(forms.Form):
    user_publisher = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__type=Profile.PUBLISHER),
    )
    publisher_company = forms.ModelChoiceField(
        queryset=PublisherCompany.objects.all())

    def save(self, commit=True):
        publisher_user = self.cleaned_data['user_publisher']
        publisher_company = self.cleaned_data['publisher_company']
        publisher_user.profile.publisher_company = publisher_company
        if commit:
            publisher_user.save()
        return publisher_user
