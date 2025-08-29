from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Infos OM Pay", {"fields": ("phone_number", "country")}),
    )
    list_display = ("username", "email", "phone_number", "is_staff")
