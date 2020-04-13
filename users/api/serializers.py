from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Profile


class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['email'].allow_blank = False
        self.fields['email'].validators = [
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.'),
        ]

        self.fields['first_name'].required = True
        self.fields['first_name'].allow_blank = False

        self.fields['last_name'].required = True
        self.fields['last_name'].allow_blank = False

    password = serializers.CharField()
    birthday = serializers.DateField(required=False)
    patronymic = serializers.CharField(default='')
    get_newsletter = serializers.BooleanField(default=False)

    def to_representation(self, instance):
        return {
            'username': instance.username,
        }

    def validate(self, attrs):
        password = attrs.get('password')

        errors = dict()
        # validate password
        try:
            validate_password(password)
        except ValidationError as e:
            errors['password'] = e.messages
        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = self.Meta.model(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.refresh_from_db()
        user.profile.patronymic = validated_data.get("patronymic")
        user.profile.birthday = validated_data.get("birthday")
        user.profile.get_newsletter = validated_data.get("get_newsletter")
        user.profile.type = Profile.READER
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "birthday",
            "password",
            "get_newsletter",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].read_only = True

        self.fields['first_name'].required = True
        self.fields['first_name'].allow_blank = False

        self.fields['last_name'].required = True
        self.fields['last_name'].allow_blank = False

    birthday = serializers.DateField(required=False)
    patronymic = serializers.CharField(default='')
    get_newsletter = serializers.BooleanField(default=False)

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'patronymic': instance.profile.patronymic,
            'email': instance.email,
            'birthday': instance.profile.birthday,
            'get_newsletter': instance.profile.get_newsletter,
        }

    def update(self, instance, validated_data):
        profile_fields = [
            "birthday",
            "patronymic",
            "get_newsletter",
        ]
        for field, value in validated_data.items():
            if field in profile_fields:
                setattr(instance.profile, field, value)
            else:
                setattr(instance, field, value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "birthday",
            "get_newsletter",
        )
