from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_users"

    def ready(self) -> None:
        from . import signals  # noqa: F401, I001
