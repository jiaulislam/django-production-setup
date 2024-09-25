from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from ..models import UserProfile


class AccountProfileSerializer(s.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ("user",)


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
    profile = AccountProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        exclude = [
            "created_on",
            "updated_on",
            "created_by",
            "updated_by",
            "is_superuser",
        ]


class RegisterAccountSerializer(s.ModelSerializer):
    first_name = s.CharField(max_length=88, allow_blank=True, default="")
    last_name = s.CharField(max_length=88, allow_blank=True, default="")
    password2 = s.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data.get("first_name"),
            last_name=self.validated_data.get("last_name"),
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise s.ValidationError({"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()
        return user


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
