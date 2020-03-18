from django.urls import path
from . import views


urlpatterns = [
    # overridden django-allauth URLs
    path('social/connections/', views.CustomConnectionsView.as_view(),
         name='socialaccount_connections'),

    # disabled django-allauth URLs
    path('social/login/cancelled/', views.login_cancelled),
]
