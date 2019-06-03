from django.apps import AppConfig


class Ford3Config(AppConfig):
    name = 'ford3'

    def ready(self):
        import ford3.signals # noqa
