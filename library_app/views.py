from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import FilteredRelation, Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from users_app.custom_mixins import UserIsPublisherAndHaveCompanyMixin

from .model_filters import BookFilter
from .models import Author, Book
from .utils import join_params_for_pagination


class BookListView(ListView):
    filterset_class = BookFilter
    queryset = Book.objects.all().prefetch_related("authors", "genres")
    paginate_by = 9
    context_object_name = "books"
    template_name = "library_app/book/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('o') in ['author', '-author']:
            queryset = queryset.annotate(
                main=FilteredRelation(
                    'bookauthorspriority',
                    condition=Q(bookauthorspriority__main=True))
            )

        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['page_params'] = join_params_for_pagination(
            self.request.GET.copy())
        return context


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "library_app/book/detail.html"


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = "author"
    template_name = "library_app/author/detail.html"


class CreateBookView(UserIsPublisherAndHaveCompanyMixin, CreateView):
    model = Book
    fields = ('title', 'cover', 'year_made', 'page_count', 'authors',
              'genres',)
    template_name = 'library_app/book/create.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        publisher_company = self.request.user.profile.publisher_company
        # Create the book with the company the user-publisher belongs to
        self.object.publisher_company = publisher_company
        self.object.save()
        messages.success(self.request, f'Book "{self.object.title}" '
                                       f'has been created.')

        return super().form_valid(form)


class DeleteBookView(UserIsPublisherAndHaveCompanyMixin, View):
    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        if request.user.profile.publisher_company == book.publisher_company:
            book.delete()
            messages.success(request, 'Book has been deleted successfully')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        raise PermissionDenied
