from django.db import models
from django.utils import timezone
from scheduler_teams.models import CustomTeam
from scheduler_app.models import CustomUser

# Create your models here.
class TeamMessage(models.Model):
    room = models.ForeignKey(CustomTeam,related_name="room_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, default="", related_name="author_messages", on_delete=models.CASCADE)
    message = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Messages"
        db_table = "teams_chat_messages"

    def __str__(self):
        return self.author.email