from rest_framework import serializers

from comments.models import Comment
from library.models import Book, Author

from .mixins import GenresFieldMixin


class AuthorSerializer(GenresFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('pseudonym', 'name', 'surname', 'patronymic',
                  'birthday', 'deathday', 'country', 'genres',
                  'biography',)


class BookAuthorSerializer(serializers.ModelSerializer):
    """Used as a nested field."""
    class Meta:
        model = Author
        fields = ('id', 'pseudonym')


class BookSerializer(GenresFieldMixin, serializers.ModelSerializer):
    publisher_company = serializers.CharField(
        source='publisher_company.name')
    ratings_average = serializers.DecimalField(
        source='ratings.first.average',
        max_digits=4,
        decimal_places=2)
    authors = BookAuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'year_made',
                  'publisher_company', 'authors', 'genres',
                  'page_count', 'ratings_average')


class CommentGETSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',
                                 read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'created_at', 'user', 'text')


class CommentPOSTSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('parent', 'created_at', 'user', 'text')
