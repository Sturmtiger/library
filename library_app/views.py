# from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Author, Book


class BookList(ListView):
    model = Book
    paginate_by = 10
    context_object_name = "books"
    template_name = "library_app/book_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all().prefetch_related(
            "authors", "genres")
        return queryset


class BookDetail(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "library_app/book_detail.html"


class AuthorDetail(DetailView):
    model = Author
    context_object_name = "author"
    template_name = "library_app/author_detail.html"
