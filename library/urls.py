from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("books/<slug:slug>/", views.BookDetailView.as_view(), name="book_detail"),
    path(
        "authors/<slug:slug>/", views.AuthorDetailView.as_view(), name="author_detail"
    ),
    path("create_book/", views.CreateBookView.as_view(), name="create_book"),
    path("delete_book/<slug:slug>/", views.BookDeleteView.as_view(), name="delete_book"),
]
