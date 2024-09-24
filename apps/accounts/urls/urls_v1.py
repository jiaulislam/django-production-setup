from django.urls import path
from rest_framework.routers import DefaultRouter

from ..views.views_v1 import (
    AccountViewSetV1,
    CookieTokenRefreshView,
    LoginView,
    LogoutView,
    MeView,
)

router = DefaultRouter()

router.register("accounts", AccountViewSetV1, basename="accounts")

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("login/", LoginView.as_view(), name="auth-login"),
        path("logout/", LogoutView.as_view(), name="auth-logout"),
        path("me/", MeView.as_view(), name="auth-me"),
        path(
            "refresh-token/",
            CookieTokenRefreshView.as_view(),
            name="auth-refresh-token",
        ),
    ]
)
