from django.conf.urls import include, url
from twotter.views import dashboard, signup, profile

urlpatterns = [
	url(r"^accounts/", include("django.contrib.auth.urls")),
	url(r"^dashboard/", dashboard, name="dashboard"),
	url(r"^profile/", profile, name="profile"),
	url(r"^signup/", signup, name="signup"),
]
