from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Message, Follow, Twoot
from .serializers import UserModelSerializer, MessageModelSerializer, FollowModelSerializer

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


def userlist(request):
    return render(request, "twotter/userlist.html")


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
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(Q(username=target))
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


class FollowModelViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowModelSerializer
    allowed_methods = ('GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        target = self.request.query_params.get('target', None)
        req = self.request.query_params.get('req', None)
        if req is None:
            self.queryset = self.queryset.filter(Q(follower=request.user, subject__username=target))
        elif req == "followers":
            self.queryset = self.queryset.filter(Q(subject__username=target))
        elif req == "following":
            self.queryset = self.queryset.filter(Q(follower__username=target))

        serialized = FollowModelSerializer(self.queryset, many=True)
        return Response(serialized.data)


def twoot_list(request):
    twoots = Twoot.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'twoot/twoot_list.html', {'twoots': twoots})


def twoot_detail(request, pk):
    twoot = get_object_or_404(Twoot, pk=pk)
    is_liked = False
    if twoot.likes.filter(id=request.user.id).exists():
        is_liked = True
    return render(request, 'twoot/twoot_detail.html', {'twoot': twoot, 'is_liked': is_liked, 'total_likes': twoot.total_likes(), })


def like_twoot(request):
    twoot = get_object_or_404(Twoot, id=request.POST.get('id'))
    is_liked = False
    if twoot.likes.filter(id=request.user.id).exists():
        twoot.likes.remove(request.user)
        is_liked = False
    else:
        twoot.likes.add(request.user)
        is_liked = True
    context = {
        'twoot': twoot,
        'is_liked': is_liked,
        'total_likes': twoot.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('twoot/likes.html', context, request=request)
        return JsonResponse({'form': html})