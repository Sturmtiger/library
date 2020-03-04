from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Profile


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        """
        Checks if user is admin and gives access to the View.
        """
        user = self.request.user
        return user.is_authenticated and user.profile.type == Profile.ADMIN
