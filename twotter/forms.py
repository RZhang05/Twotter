from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from .models import User
from django import forms


class CustomUserChangeForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'status', 'user_img']
			
	def clean_user_img(self):
		try:
			user_img = self.cleaned_data['user_img']
			h = user_img.height_field
			w = user_img.width_field

			max_width = max_height = 1000
			if w > max_width or h > max_height:
				raise forms.ValidationError('Please use an image that is ' + max_width + ' by ' + max_height + ' or smaller.')
		
			main, sub = user_img.content_type.split('/')
			if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
				raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')
		
		except AttributeError:
			pass
		
		return user_img	


class CustomUserCreationForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'status', 'user_img']
		widgets = {
			'password': forms.PasswordInput,
		}

	def clean_user_img(self):
		try:
			user_img = self.cleaned_data['user_img']
			h = user_img.height_field
			w = user_img.width_field

			max_width = max_height = 1000
			if w > max_width or h > max_height:
				raise forms.ValidationError('Please use an image that is ' + max_width + ' by ' + max_height + ' or smaller.')
		
			main, sub = user_img.content_type.split('/')
			if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
				raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')
		
		except AttributeError:
			pass
		
		return user_img

	def save(self, commit=True):
		user=super(CustomUserCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
