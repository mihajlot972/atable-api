from rest_framework import generics
from rest_framework.response import Response
from scheduler_chat.models import TeamMessage
from scheduler_teams.models import CustomTeam
from scheduler_chat.serializers import ChatSerializer


class ChatView(generics.GenericAPIView):
    serializer_class = ChatSerializer

#
# def get_team_id(self, team_id):
#     team_id = CustomTeam.objects.get(id=team_id)