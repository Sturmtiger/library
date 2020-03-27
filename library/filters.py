import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="iexact")

    o = django_filters.OrderingFilter(
        fields=(
            ("title", "title"),
            ("year_made", "year_made"),
            ("publisher_company__name", "publisher_company"),
            ("main__author__pseudonym", "author"),
            ("ratings__average", "ratings"),
        )
    )

    class Meta:
        model = Book
        fields = ("title", "year_made", "publisher_company", "authors")
