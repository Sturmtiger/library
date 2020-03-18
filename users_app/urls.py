from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .custom_django_allauth.account.urls import urlpatterns \
    as account_overridden_urls
from .custom_django_allauth.socialaccount.urls import urlpatterns \
    as socialaccount_overridden_urls


urlpatterns = [
    path("admin_panel/", views.AdminPanelView.as_view(), name="admin_panel"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("update_user/", views.UpdateUserView.as_view(), name="update_user"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users_app/password_change/form.html"
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users_app/password_change/done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password/reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users_app/password_reset/done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users_app/password_reset/complete.html"
        ),
        name="password_reset_complete",
    ),
]

urlpatterns += account_overridden_urls
urlpatterns += socialaccount_overridden_urls