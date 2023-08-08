from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from users.models import User


admin.site.unregister(Group)


@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "user_type",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "user_type",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "user_type",
                    "email",
                    "username",
                    "password",
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "user_type")
    search_fields = ("username", "email")
    ordering = ("email",)
    filter_horizontal = []
