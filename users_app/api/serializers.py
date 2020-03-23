from rest_framework import serializers
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserModel
        fields = ('url', 'id', 'slug', 'title', 'year_made', 'page_count')
