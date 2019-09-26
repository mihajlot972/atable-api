from django.db import models
from django.contrib.auth.models import AbstractUser
from scheduler_teams.models import CustomTeam

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_team_creator = models.BooleanField(default=False)
    teams = models.ManyToManyField(CustomTeam, related_name='all_team_id')
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = "Users"
        db_table = 'users'

    
    def __str__(self):
        return self.email




