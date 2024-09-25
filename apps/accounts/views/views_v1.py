from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions as e
from rest_framework import response as r
from rest_framework import status as s
from rest_framework import viewsets as vs
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from ..serializers.accounts_v1 import (
    AccountSerializerV1,
    CookieTokenRefreshSerializer,
    LoginSerializer,
    RegisterAccountSerializer,
)
from ..services import auth_cookies, generate_user_token, remove_auth_cookies


class AccountViewSetV1(vs.ModelViewSet):
    serializer_class = AccountSerializerV1
    permission_class = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return get_user_model().objects.filter(is_superuser=False)


class RegisterAccountView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterAccountSerializer

    def post(self, request, format=None):
        body = RegisterAccountSerializer(data=request.data)
        body.is_valid(raise_exception=True)

        user = body.save()

        if user is None:
            return r.Response(
                {"status": "error", "msg": "create user failed !"},
                status=s.HTTP_400_BAD_REQUEST,
            )
        return r.Response(
            {"status": "success", "msg": "account created"},
            status=s.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    @auth_cookies
    def post(self, request, format=None):
        body = LoginSerializer(data=request.data)

        body.is_valid(raise_exception=True)

        email = body.validated_data["email"]
        password = body.validated_data["password"]

        authorized_user = authenticate(request, email=email, password=password)

        if authorized_user is None:
            raise e.AuthenticationFailed("Email or Password is incorrect")

        tokens = generate_user_token(authorized_user)

        return r.Response(tokens)


class LogoutView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @remove_auth_cookies
    def post(self, request, format=None):
        return r.Response(status=s.HTTP_204_NO_CONTENT)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            del response.data["refresh"]

        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


class MeView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializerV1

    def get(self, request, *args, **kwargs):
        return r.Response(AccountSerializerV1(instance=request.user).data)
