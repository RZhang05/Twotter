from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from twotter.forms import CustomUserCreationForm
from twotter.models import User

# Create your views here.
def profile(request, username):
	try:
		user = User.objects.get(username=username);
	except:
		#in reality raise 404
		return render(request, 'twotter/dashboard.html')
	
	editPerms = False
	if request.user.is_authenticated and request.user==user:
		editPerms = True
	
	context = locals()
	return render(request, 'twotter/profile.html', context)

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
