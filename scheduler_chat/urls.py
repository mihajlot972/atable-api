from django.urls import path
from scheduler_chat.views import ChatView

urlpatterns = [
    path('', ChatView.as_view(), name='chat')
]
