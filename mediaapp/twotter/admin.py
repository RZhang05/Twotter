from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User as CustomUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        ('Account Info', {'fields': ('email', 'username', 'password', 'date_joined')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Extra', {'fields': ('status', 'img_name')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
