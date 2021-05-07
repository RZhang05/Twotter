from twotter.models import User
from rest_framework.serializers import ModelSerializer

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
