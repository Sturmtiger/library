from django.apps import AppConfig


class LibraryAppConfig(AppConfig):
    name = "library_app"

    def ready(self):
        from . import signal_handlers
