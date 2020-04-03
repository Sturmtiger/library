from django.contrib.auth.models import User
from django.db import models

from library.models import PublisherCompany


class Profile(models.Model):
    ADMIN = 1
    PUBLISHER = 2
    READER = 3
    TYPE_CHOICES = ((ADMIN, "admin"), (PUBLISHER, "publisher"), (READER, "reader"))

    # This field is used only for user-publisher, it is NULL to defaults.
    # You can set a publisher-company for a user-publisher from the admin-panel
    publisher_company = models.ForeignKey(
        PublisherCompany, null=True, blank=True, on_delete=models.SET_NULL
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # By default, a reader type is created
    # to avoid the issue of not having a user type.
    type = models.IntegerField(choices=TYPE_CHOICES, default=READER)
    birthday = models.DateField(null=True, blank=True)
    patronymic = models.CharField(max_length=50, blank=True)
    get_newsletter = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.user.username}({self.user.id})"
