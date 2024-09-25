from functools import wraps

from django.conf import settings as s
from django.contrib.auth.models import AbstractBaseUser
from django.middleware import csrf
from rest_framework.request import Request
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken


def generate_user_token(user: AbstractBaseUser):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
        "iat": refresh.get("iat"),
        "exp": refresh.get("exp"),
    }


def auth_cookies(view_func):
    @wraps(view_func)
    def _wrapper(self, request: Request, *args, **kwargs):
        response = view_func(self, request, *args, **kwargs)
        access_token = response.data.get("access_token")
        refresh_token = response.data.get("refresh_token")

        response.set_cookie(
            key=s.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            expires=s.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=s.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=s.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
            samesite=s.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        response.set_cookie(
            key=s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=refresh_token,
            expires=s.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=s.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=s.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
            samesite=s.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response["X-CSRFToken"] = csrf.get_token(request)
        return response

    return _wrapper


def remove_auth_cookies(view_func):
    @wraps(view_func)
    def _wrapper(self, request: Request, *args, **kwargs):
        response = view_func(self, request, *args, **kwargs)
        refresh_token = request.COOKIES.get(s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])

        token = tokens.RefreshToken(refresh_token)
        token.blacklist()

        response.delete_cookie(s.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        response.delete_cookie("X-CSRFToken")
        response.delete_cookie("csrftoken")
        response["X-CSRFToken"] = None
        return response

    return _wrapper
