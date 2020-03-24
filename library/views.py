from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import FilteredRelation, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin

from comments.forms import CommentForm
from comments.models import Comment
from users.custom_mixins import UserIsPublisherAndHaveCompany

from .filters import BookFilter
from .models import Author, Book, BookAuthorsPriority
from .utils import join_params_for_pagination


class BookListView(ListView):
    filterset_class = BookFilter
    queryset = Book.objects.all().prefetch_related("authors", "genres")
    paginate_by = 9
    context_object_name = "books"
    template_name = "library/book/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get("o") in ["author", "-author"]:
            queryset = queryset.annotate(
                main=FilteredRelation(
                    "bookauthorspriority", condition=Q(bookauthorspriority__priority=1)
                )
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        context["page_params"] = join_params_for_pagination(self.request.GET.copy())
        return context


@method_decorator(csrf_protect, name="dispatch")
class BookDetailView(FormMixin, DetailView):
    model = Book
    form_class = CommentForm

    context_object_name = "book"
    template_name = "library/book/detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url_param = "?next=%s" % request.path
            return HttpResponseRedirect(reverse("login") + next_url_param)
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().select_related("user")
        return context

    def form_valid(self, form):
        parent = None
        parent_id = self.request.POST.get("parent")
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)

        comment = form.save(commit=False)
        comment.content_object = self.object
        comment.user = self.request.user
        comment.parent = parent
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("library:book_detail", kwargs={"slug": self.object.slug})


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = "author"
    template_name = "library/author/detail.html"


class CreateBookView(UserIsPublisherAndHaveCompany, CreateView):
    model = Book
    fields = ("title", "cover", "year_made", "page_count", "authors", "genres")
    template_name = "library/book/create.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return self.request.GET.get("next", "/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "/")
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        publisher_company = self.request.user.profile.publisher_company
        # Create the book with the company the user-publisher belongs to
        self.object.publisher_company = publisher_company
        self.object.save()

        # create author priority in the through model
        for author in form.cleaned_data.get("authors"):
            BookAuthorsPriority.objects.create(book=self.object, author=author)

        messages.success(
            self.request, f'Book "{self.object.title}" ' f"has been created."
        )
        return super().form_valid(form)


class BookDeleteView(UserIsPublisherAndHaveCompany, DeleteView):
    model = Book

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        if request.user.profile.publisher_company == book.publisher_company:
            messages.success(request, "Book has been deleted successfully")
            return super().delete(request, *args, **kwargs)
        raise PermissionDenied

    def get_success_url(self):
        next_url = self.request.GET.get("next", "/")
        return next_url
