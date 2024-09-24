from django.contrib import admin
from django.urls import include, path

api_v1 = "api/v1/"
api_v2 = "api/v2/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(api_v1, include(("apps.accounts.urls.urls_v1", "accounts"), namespace="v1")),
    path(api_v2, include(("apps.accounts.urls.urls_v2", "accounts"), namespace="v2")),
]
