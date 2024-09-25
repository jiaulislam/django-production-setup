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
]

v1_routes = [
    path(api_v1, include(("apps.accounts.urls.urls_v1", "accounts"), namespace="v1")),
    path(
        f"{api_v1}schema/",
        SpectacularAPIView.as_view(
            api_version="v1", renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
        ),
        name="schema-v1",
    ),
    path(
        f"{api_v1}docs/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-ui",
    ),
    path(
        f"{api_v1}redoc/",
        SpectacularRedocView.as_view(url_name="schema-v1"),
        name="redoc",
    ),
]

v2_routes = [
    path(api_v2, include(("apps.accounts.urls.urls_v2", "accounts"), namespace="v2")),
    path(
        f"{api_v2}schema/",
        SpectacularAPIView.as_view(
            api_version="v2", renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
        ),
        name="schema-v2",
    ),
    path(
        f"{api_v2}docs/",
        SpectacularSwaggerView.as_view(url_name="schema-v2"),
        name="swagger-v2",
    ),
    path(
        f"{api_v2}redoc/",
        SpectacularRedocView.as_view(url_name="schema-v2"),
        name="redoc",
    ),
]


versioned_routes = [v1_routes, v2_routes]

for routes in versioned_routes:
    urlpatterns.extend(routes)
