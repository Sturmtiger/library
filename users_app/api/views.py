from rest_framework.viewsets import ModelViewSet

from .serializers import BookSerializer
from library_app.models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    