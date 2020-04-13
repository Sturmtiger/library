from django_filters import rest_framework as filters

from ..models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="iexact")
    publisher_company = filters.CharFilter(
        field_name="publisher_company__name",
        lookup_expr="icontains")

    o = filters.OrderingFilter(
        fields=(
            ("title", "title"),
            ("year_made", "year_made"),
            ("publisher_company__name", "publisher_company"),
            ("ratings__average", "ratings"),
        )
    )

    class Meta:
        model = Book
        fields = ("title", "year_made", "publisher_company")
