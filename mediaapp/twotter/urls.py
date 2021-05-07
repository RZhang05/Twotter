from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter
from twotter.views import UserModelViewSet

router = DefaultRouter()
router.register(r'user', UserModelViewSet, basename = 'user-api')

urlpatterns = [
	path("accounts/", include("django.contrib.auth.urls")),
	path("dashboard/", views.dashboard,name="dashboard"),
	path('profile/<username>/', views.profile, name="profile"),
	path("signup/", views.signup,name="signup"),
	path('edit/<username>/', views.edit_profile, name="edit_profile"),
	path('chat/<str:room_name>/', views.chat, name='chat'),
	
	path(r'api/', include(router.urls)),
]
