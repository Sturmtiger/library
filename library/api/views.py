from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer, CommentSerializer
from library.models import Book
from comments.models import Comment
from .filters import BookFilter


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter


class CommentOfBookListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.validated_data.get('parent')
        if comment and comment not in self.get_queryset():
            return Response(
                {'detail': 'a comment of book with id matching '
                           'the specified parent id was not found.',
                 },
                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        # The book the comment belongs to
        book = Book.objects.get(pk=self.kwargs.get('pk'))

        serializer.save(user=user, content_object=book)

    def get_queryset(self):
        book = self.kwargs['pk']
        queryset = Comment.objects.filter(book=book)
        return queryset
