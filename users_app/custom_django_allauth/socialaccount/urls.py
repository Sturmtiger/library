from django.urls import path
from . import views


urlpatterns = [
    # disabled django-allauth URLs
    path('social/login/cancelled/', views.login_cancelled),
]
