from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from scheduler_teams.models import CustomTeam
from scheduler_app.models import CustomUser
from scheduler_chat.models import TeamMessage
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict
import json

class ChatConsumer(WebsocketConsumer):


    def retrieve_15(self, chatId):
        team_id = TeamMessage.objects.filter(room_id=chatId)[:15]
        return team_id


    def fetch_messages(self, data):
        messages = self.retrieve_15(data['team_id'])
        content = {
            'command': 'messages',
            'message': self.messages_to_json(messages) 
        }
        self.send_message(content)

    def new_message(self, data):
        print(data)
        author = CustomUser.objects.get(id=self.user_id)
        room = CustomTeam.objects.get(id=self.team_id)
        message = TeamMessage.objects.create(room=room, author=author, message=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    
    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'content': message.message,
            'room': message.room.team_name,
            'timestamp': str(message.timestamp)
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.room_group_name = 'chat_%s' % self.team_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        print(type(data))
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))