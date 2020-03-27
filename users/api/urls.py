from django.urls import path, re_path

from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    re_path(r'^api-auth-token/', obtain_auth_token),
]
