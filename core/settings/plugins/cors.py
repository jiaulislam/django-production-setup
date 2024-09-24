from corsheaders.defaults import default_headers

from core.env import env

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default=[])

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)


CORS_ALLOW_HEADERS = (*default_headers, "x-sha-256", "x-sha-512", "x-signature")

CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
