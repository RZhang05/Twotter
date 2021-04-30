from django.conf.urls import include, url
from twotter.views import dashboard, signup

urlpatterns = [
	url(r"^accounts/", include("django.contrib.auth.urls")),
	url(r"^dashboard/", dashboard, name="dashboard"),
	url(r"^signup/", signup, name="signup"),
]
