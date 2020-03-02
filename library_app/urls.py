from django.urls import path
from . import views

app_name = "library_app"

urlpatterns = [
    path("",
         views.BookList.as_view(),
         name="book_list"),
    path("books/<slug:slug>/",
         views.BookDetail.as_view(),
         name="book_detail"),
    path("authors/<slug:slug>/",
         views.AuthorDetail.as_view(),
         name="author_detail"),
]
