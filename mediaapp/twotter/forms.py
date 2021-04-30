from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('date_of_birth', 'status', 'img_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('date_of_birth', 'status', 'img_name',)

