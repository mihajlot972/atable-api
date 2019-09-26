from rest_framework import serializers
from scheduler_teams.models import CustomTeam, Atable
from scheduler_app.models import CustomUser
from scheduler_tasks.models import Tasks, TasksComments


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('task_name', 'task_description', 'time_estimate', 'time_spent')

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksComments
        fields = ('task_comment',)