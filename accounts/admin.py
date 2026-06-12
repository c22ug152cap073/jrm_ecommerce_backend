from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = ("email",)

    ordering = ("email",)