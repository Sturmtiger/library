from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('books/<pk>/comments/', views.CommentOfBookList.as_view(),
         name='comment-of-book-list'),
]

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns += router.urls
