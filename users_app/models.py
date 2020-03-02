from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ADMIN = 1
    PUBLISHER = 2
    READER = 3
    TYPE_CHOICES = (
        (ADMIN, 'admin'),
        (PUBLISHER, 'publisher'),
        (READER, 'reader'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    birthday = models.DateField()
    patronymic = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username}({self.user.id})'
