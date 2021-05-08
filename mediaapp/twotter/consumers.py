import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		user_id = self.scope["session"]["_auth_user_id"]
		self.group_name = "{}".format(user_id)

		# Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.group_name,
			self.channel_name
		)

		self.accept()

	def disconnect(self, close_code):
		# Leave room group
		async_to_sync(self.channel_layer.group_discard)(
			self.group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Send message to room group
		async_to_sync(self.channel_layer.group_send)(
			self.group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)

	# Receive message from room group
	def chat_message(self, event):
		message = event['message']

		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'message': message
		}))
