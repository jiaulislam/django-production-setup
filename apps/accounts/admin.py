from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import UserAccount, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    show_change_link = True


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone"]


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "date_joined",
        "is_admin",
        "is_superuser",
        "is_active",
    )
    search_fields = ("email", "first_name", "last_name")
    inlines = [ProfileInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "New User",
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ("date_joined",)
    list_filter = ("is_admin", "is_superuser")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def save_model(
        self, request: HttpRequest, obj: UserAccount, form: ModelForm, change: bool
    ) -> None:
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
