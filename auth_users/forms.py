from django.contrib.auth.forms import UserChangeForm

from .models import ExtendedUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = ExtendedUser
        fields = "__all__"
