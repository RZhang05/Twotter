from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class User(AbstractUser):
	date_of_birth = models.DateField(null=True, help_text='YYYY-MM-DD')
	status = models.TextField(max_length=100,blank=True,help_text='Optional.')
	user_img = models.ImageField(upload_to='images/', default = 'default.jpg')

	def __str__(self):
		return self.username

	def get_followers(self):
		return Follow.objects.filter(subject=self)

	def get_following(self):
		return Follow.objects.filter(follower=self)


class Follow(models.Model):
	timestamp =  models.DateTimeField(auto_now_add=True, editable = False)
	subject = models.ForeignKey(User, related_name = "subject", on_delete=models.CASCADE)
	follower = models.ForeignKey(User, related_name = "follower", on_delete=models.CASCADE)


class Twoot(models.Model):
	content = models.TextField(max_length=280)
	created_date = models.DateTimeField(default=timezone.now())
	published_date = models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	slug = models.SlugField(unique=True, blank=True)

	def __str__(self):
		return self.content

	def total_likes(self):
		return self.likes.count()


class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', db_index=True)
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
	body = models.TextField()

	def __str__(self):
		return str(self.id)

	def notify(self):
		channel_layer = get_channel_layer()
		notification = {
			'type': 'chat_message',
			'message': '{}'.format(self.id)	
		}
		async_to_sync(channel_layer.group_send)("{}".format(self.sender.id), notification)
		async_to_sync(channel_layer.group_send)("{}".format(self.receiver.id), notification) 

	def save(self, *args, **kwargs):
		new = self.id
		super(Message, self).save(*args, **kwargs)
		if new is None:
			self.notify()
