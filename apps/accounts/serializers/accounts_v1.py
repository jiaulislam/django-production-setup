from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class AccountSerializerV1(s.ModelSerializer):
    password = s.CharField(write_only=True)
    date_joined = s.DateTimeField(read_only=True)
    is_admin = s.BooleanField(read_only=True)
    email = s.EmailField(read_only=True)
    last_login = s.DateTimeField(read_only=True)
    groups = s.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )
    user_permissions = s.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        exclude = [
            "created_on",
            "updated_on",
            "created_by",
            "updated_by",
            "is_superuser",
        ]


class LoginSerializer(s.Serializer):
    email = s.EmailField()
    password = s.CharField(style={"input_type": "password"}, write_only=True)


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh'")
