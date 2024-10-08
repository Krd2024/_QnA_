from django.apps import AppConfig


class DjangoRedisConfig(AppConfig):
    name = "django_redis"
    verbose_name = "Django Redis"


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):

        from . import signals  # noqa: F401
