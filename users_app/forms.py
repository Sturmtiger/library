from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile
from .utils import gen_username_from_email


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    birthday = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
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

    def save(self, commit=True):
        user = super().save(commit=False)

        username = gen_username_from_email(self.cleaned_data['email'])

        user.username = username
        user.set_unusable_password()
        if commit:
            user.save()
            user.profile.type = Profile.PUBLISHER
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email
