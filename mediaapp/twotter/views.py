from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Message
from .serializers import UserModelSerializer, MessageModelSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication


# Create your views here.
def profile(request, username):
    try:
        user = User.objects.get(username=username);
    except:
        # in reality raise 404
        return render(request, 'twotter/dashboard.html')

    editPerms = False
    if request.user.is_authenticated and request.user == user:
        editPerms = True

    context = locals()
    return render(request, 'twotter/profile.html', context)


def dashboard(request):
    return render(request, 'twotter/dashboard.html')


@login_required
def edit_profile(request, username):
    user = request.user
    form = CustomUserChangeForm(request.POST or None,
                                initial={'first_name': user.first_name, 'last_name': user.last_name,
                                         'email': user.email, 'status': user.status
                                    , 'user_img': user.user_img})
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
    form = CustomUserCreationForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))

    return render(request, "twotter/signup.html", {"form": form})


def chat(request):
    return render(request, "twotter/chat.html")


# API
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.exclude(username=request.user.username)
        serialized = UserModelSerializer(self.queryset, many=True)
        return Response(serialized.data)


class MessagePagination(PageNumberPagination):
    page_size = 20


class CsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(receiver=request.user) | Q(sender=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(Q(receiver=request.user, sender__username=target) |
                                                 Q(receiver__username=target, sender=request.user))
        serialized = MessageModelSerializer(self.queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(receiver=request.user) | Q(sender=request.user), Q(pk=kwargs['pk']))
        )
        serialized = MessageModelSerializer(msg)
        return Response(serialized.data)
