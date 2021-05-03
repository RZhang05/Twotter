from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

class User(AbstractUser):
	date_of_birth = models.DateField(null=True, help_text='YYYY-MM-DD')
	status = models.TextField(max_length=100,blank=True,help_text='Optional.')
	user_img = models.ImageField(upload_to='images/', default = 'default.jpg')

	def __str__(self):
		return self.username
