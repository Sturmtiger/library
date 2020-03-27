from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
]
