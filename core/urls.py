from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.settings import api_settings

api_v1 = "api/v1/"
api_v2 = "api/v2/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(api_v1, include(("apps.accounts.urls.urls_v1", "accounts"), namespace="v1")),
    path(api_v2, include(("apps.accounts.urls.urls_v2", "accounts"), namespace="v2")),
]

v1_schemas = [
    path(
        f"{api_v1}schema/",
        SpectacularAPIView.as_view(
            api_version="v1", renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
        ),
        name="schema",
    ),
    path(
        f"{api_v1}schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{api_v1}schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns.extend(v1_schemas)
