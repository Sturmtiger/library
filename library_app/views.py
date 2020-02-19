# from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .model_filters import BookFilter
from .models import Author, Book
from .utils import join_params_for_pagination


class BookList(ListView):
    filter = None
    filterset_class = BookFilter
    queryset = Book.objects.all().prefetch_related("authors", "genres")
    paginate_by = 2
    context_object_name = "books"
    template_name = "library_app/book_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = self.filterset_class(
            self.request.GET,
            queryset=queryset
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['page_params'] = join_params_for_pagination(
            self.request.GET.copy())
        return context


class BookDetail(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "library_app/book_detail.html"


class AuthorDetail(DetailView):
    model = Author
    context_object_name = "author"
    template_name = "library_app/author_detail.html"
