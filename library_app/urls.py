from django.urls import path

from . import views

app_name = "library_app"

urlpatterns = [
    path("",
         views.BookList.as_view(),
         name="book-list"),
    path("book/<slug:slug>/",
         views.BookDetail.as_view(),
         name="book-detail"),
    path("author/<slug:slug>/",
         views.AuthorDetail.as_view(),
         name="author-detail"),
]
