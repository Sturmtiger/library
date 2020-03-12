from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile


class UserIsAdminMixin(UserPassesTestMixin):
    """
    Checks if user is admin.
    """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.profile.type == Profile.ADMIN


class UserIsPublisherAndHaveCompanyMixin(LoginRequiredMixin):
    """
    Verify that the current user is authenticated, is publisher
    and has publisher company.
    """
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if (user.is_authenticated
                and user.profile.type == Profile.PUBLISHER
                and user.profile.publisher_company):
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class UserIsNotLoggedIn(UserPassesTestMixin):
    """
    Checks if user is not logged in.
    """
    def test_func(self):
        user = self.request.user
        return not user.is_authenticated
