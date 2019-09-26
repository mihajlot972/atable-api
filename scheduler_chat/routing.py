from scheduler_chat.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    # path('ws/chat/', ChatConsumer),
    path('ws/chat/<int:user_id>/<int:team_id>/', ChatConsumer),
]