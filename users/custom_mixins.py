from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Profile


class UserIsAdmin(UserPassesTestMixin):
    """
    Checks if user is admin.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.profile.type == Profile.ADMIN


class UserIsPublisherAndHaveCompany(LoginRequiredMixin):
    """
    Verify that the current user is authenticated, is publisher
    and has publisher company.
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if (
            user.is_authenticated
            and user.profile.type == Profile.PUBLISHER
            and user.profile.publisher_company
        ):
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class PublisherCanDeleteBook(UserIsPublisherAndHaveCompany):
    """
    Checks if user's publisher-company corresponds to
    the publisher-company of the book.
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        book = self.get_object()
        if user.profile.publisher_company == book.publisher_company:
            return super().post(request, *args, **kwargs)
        raise PermissionDenied


class AnonymousUserRequired(UserPassesTestMixin):
    """
    Checks if user is not logged in.
    """

    def test_func(self):
        user = self.request.user
        return user.is_anonymous


class CurrentUserObjectMixin:
    def get_object(self, queryset=None):
        return self.request.user
