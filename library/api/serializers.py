from rest_framework import serializers

from comments.models import Comment
from library.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    publisher_company = serializers.CharField(
        source='publisher_company.name')
    ratings_average = serializers.DecimalField(
        source='ratings.first.average',
        max_digits=4,
        decimal_places=2)
    authors = serializers.SerializerMethodField()

    def get_authors(self, obj):
        authors = obj.authors.values_list('pseudonym', flat=True)
        return authors

    class Meta:
        model = Book
        fields = ('url', 'id', 'slug', 'title', 'year_made',
                  'publisher_company', 'authors', 'page_count', 'ratings_average')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',
                                 read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'created_at', 'user', 'text')
