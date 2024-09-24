from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..serializers.accounts_v2 import AccountSerializerV2


class AccountViewSetV2(ModelViewSet):
    serializer_class = AccountSerializerV2
    permission_class = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return get_user_model().objects.all()
