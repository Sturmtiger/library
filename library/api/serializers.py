from rest_framework import serializers

from comments.models import Comment
from library.models import Book, Author


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',
                                 read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'created_at', 'user', 'text')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'pseudonym')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'id', 'slug', 'title', 'year_made', 'page_count')
