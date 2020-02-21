import django_filters
from django_filters.constants import EMPTY_VALUES
from django.db.models import FilteredRelation, Q
from .models import Book


class CustomOrderingFilter(django_filters.OrderingFilter):
    """
    Added specific ordering by author for Book model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('main__author__pseudonym', 'Author'),
            ('-main__author__pseudonym', 'Author (descending)'),
        ]

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if any(v in ['main__author__pseudonym',
                     '-main__author__pseudonym'] for v in value):
            ordering = [self.get_ordering_value(param) for param in value]
            return qs.annotate(
                main=FilteredRelation('bookauthorspriority',
                                      condition=Q(
                                          bookauthorspriority__main=True))
            ).order_by(*ordering)

        return super().filter(qs, value)


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="iexact")

    o = CustomOrderingFilter(
        fields=(
            ("title", "title"),
            ("year_made", "year_made"),
            ("publisher_company", "publisher_company"),
        )
    )

    class Meta:
        model = Book
        fields = ("title", "year_made", "publisher_company", "authors")
