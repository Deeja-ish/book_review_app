from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", 'last_name', "email", "is_verified", "created_at")

    list_filter = ("is_verified", )