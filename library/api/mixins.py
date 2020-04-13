from rest_framework import serializers


class GenresFieldMixin(metaclass=serializers.SerializerMetaclass):
    genres = serializers.SerializerMethodField()

    def get_genres(self, obj):
        genres = obj.genres.values_list('name', flat=True)
        return genres
