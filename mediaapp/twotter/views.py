from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from twotter.forms import CustomUserCreationForm, CustomUserChangeForm
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
	users = User.objects.exclude(username=request.user.username)
	return render(request, 'twotter/dashboard.html',{"user_list":users})

@login_required
def edit_profile(request, username):
	user = request.user
	form = CustomUserChangeForm(request.POST or None, 
	initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email, 'status':user.status
	, 'user_img':user.user_img})
	if request.method == "POST":
		form = CustomUserChangeForm(request.POST, request.FILES)
		if form.is_valid():
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.status = request.POST['status']
			print(request.FILES)
			user.user_img = request.FILES['user_img']
			user.save()
			return redirect(reverse("profile", args=[username]))
	return render(request, "twotter/edit_profile.html", {"form": form})

def signup(request):
	form=CustomUserCreationForm(request.POST or None, request.FILES)
	if request.method == "POST":
		if form.is_valid():
			user = form.save()
			login(request,user)
			return redirect(reverse("dashboard"))
	
	return render(request, "twotter/signup.html",{"form":form})

def chat(request, room_name):
	return render(request, "twotter/chat.html", {"room_name": room_name})



