from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin:
    fields = ('username', 'first_name', 'last_name', 'password', 'date_of_birth', 'date_joined', 'status', 'img_name')


admin.register(User, UserAdmin)