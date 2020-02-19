import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ("title", "year_made", "publisher_company", "authors")
