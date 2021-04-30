from django.forms import ModelForm
from twotter.models import User
from django import forms



class CustomUserCreationForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'status']
		widgets = {
			'password': forms.PasswordInput,
		}

	def save(self, commit=True):
		user=super(CustomUserCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
