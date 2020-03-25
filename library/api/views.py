from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer, CommentSerializer, AuthorSerializer
from library.models import Book, Author
from comments.models import Comment


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CommentOfBookList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        parent_comment = serializer.validated_data['parent']

        if parent_comment not in self.queryset:
            return Response(
                {'detail': 'a comment with an id matching '
                           'the specified parent_id was not found.',
                 },
                status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        # The book the comment belongs to
        book = Book.objects.get(pk=self.kwargs.get('pk'))

        serializer.save(user=user, content_object=book)

    def get_queryset(self):
        book = self.kwargs['pk']
        queryset = Comment.objects.filter(book=book)
        return queryset


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'books'
