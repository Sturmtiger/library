from django.apps import AppConfig


class LibraryConfig(AppConfig):
    name = "library"

    def ready(self):
        from . import signals
