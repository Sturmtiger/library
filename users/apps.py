from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        from django.contrib.auth.models import User
        from .signals import create_user_profile, save_user_profile

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)
