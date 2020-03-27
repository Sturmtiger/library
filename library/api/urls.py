from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('books/<pk>/comments/',
         views.CommentOfBookListView.as_view(),
         name='comment_list_of_book'),
]

router = DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns += router.urls
