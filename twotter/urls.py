from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, MessageModelViewSet, FollowModelViewSet

router = DefaultRouter()
router.register(r'user', UserModelViewSet, basename = 'user-api')
router.register(r'message', MessageModelViewSet, basename = 'message-api')
router.register(r'follow', FollowModelViewSet, basename = 'follow-api')

urlpatterns = [
	path("accounts/", include("django.contrib.auth.urls")),
	path("dashboard/", views.dashboard,name="dashboard"),
	path('profile/<username>/', views.profile, name="profile"),
	path("signup/", views.signup,name="signup"),
	path('edit/<username>/', views.edit_profile, name="edit_profile"),
	path('chat/', views.chat, name='chat'),
	path('users/', views.userlist, name = 'userlist'),
	
	path(r'api/', include(router.urls)),
]
