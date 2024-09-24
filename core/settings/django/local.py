from core.env import BASE_DIR

from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
