from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "full_name", "currency", "is_staff"]
    list_filter = ["is_staff", "is_active", "currency"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-created_at"]
