from twotter.models import User, Message
from rest_framework.serializers import ModelSerializer, CharField
from django.shortcuts import get_object_or_404

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class MessageModelSerializer(ModelSerializer):
	sender = CharField(source = 'sender.username', read_only = True)
	receiver = CharField(source = 'receiver.username')
	
	def create(self, validated_data):
		print(validated_data)
		sender = self.context['request'].user
		receiver = get_object_or_404(User, username=validated_data['receiver']['username'])
		msg = Message(receiver=receiver, body=validated_data['body'], sender = sender)
		msg.save()
		return msg

	class Meta:
		model = Message
		fields = ('id', 'sender', 'receiver', 'timestamp', 'body')
