from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.TextField(max_length=100,blank=True)
    img_name = models.TextField(max_length=500,blank=True)
