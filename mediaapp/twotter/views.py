from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from twotter.forms import CustomUserCreationForm

# Create your views here.
def dashboard(request):
	return render(request, 'twotter/dashboard.html')

def signup(request):
	form=CustomUserCreationForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			user = form.save()
			login(request,user)
			return redirect(reverse("dashboard"))
	
	return render(request, "twotter/signup.html",{"form":form})
