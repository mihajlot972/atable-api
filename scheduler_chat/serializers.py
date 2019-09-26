from rest_framework import serializers
from scheduler_chat.models import TeamMessage

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMessage
        fields = ('room', 'author', 'message', 'timestamp')
        