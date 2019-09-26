from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from scheduler_app.models import CustomUser
from scheduler_teams.models import CustomTeam, Atable
from scheduler_chat.models import TeamMessage
from scheduler_tasks.models import TasksComments

class CustomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Username', {"fields": ['username']}),
        ('Email', {"fields": ['email']}),
        ('Password', {"fields": ['password']}),
        ('Is team creator', {"fields": ['is_team_creator']}),
        ('List of teams', {"fields": ['teams']}),
        ('Is superuser', {"fields": ['is_staff']}),
    ]
# Register your models here.
admin.site.register(TeamMessage)
admin.site.register(CustomTeam)
admin.site.register(Atable)
admin.site.register(CustomUser, CustomAdmin)
admin.site.register(TasksComments)
