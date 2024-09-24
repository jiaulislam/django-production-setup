from django.contrib.auth import get_user_model
from rest_framework import serializers as s


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
