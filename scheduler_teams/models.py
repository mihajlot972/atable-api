from django.db import models
from django.utils import timezone
from datetime import datetime

class CustomTeam(models.Model):
    team_name = models.CharField(max_length=15, unique=True)
    invite_url = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Teams"
        db_table = "teams"

    def __str__(self):
        return self.team_name


class Atable(models.Model):
    date = models.DateField(default=datetime.now)
    start_time = models.CharField("Start time", max_length=15, blank=True, null=True)
    end_time = models.CharField("End time", max_length=15, blank=True, null=True)
    user = models.ForeignKey('scheduler_app.CustomUser', on_delete = models.CASCADE, related_name='atable_user')
    team = models.ForeignKey(CustomTeam, on_delete = models.CASCADE, related_name='atable_team')

    class Meta:
        verbose_name_plural = 'Atable'
        db_table = "atable"
        ordering=['date']

    def __str__(self):
        return self.user.email + ' - ' + self.team.team_name
