from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User as CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Account Info', {'fields': ('email', 'username', 'password', 'date_joined')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Extra', {'fields': ('status', 'user_img')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
