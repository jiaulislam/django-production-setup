from typing import Any

from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from .forms import CustomUserChangeForm

# Register your models here.
from .models import ExtendedUser, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    show_change_link = True


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone"]

@admin.register(ExtendedUser)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "date_joined",
        "is_admin",
        "is_superuser",
        "is_active",
    ]
    inlines = [ProfileInline]
    form = CustomUserChangeForm
    def save_model(
        self, request: HttpRequest, obj: Any, form: ModelForm, change: bool
    ) -> None:
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
