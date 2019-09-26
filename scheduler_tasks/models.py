from django.db import models

# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=120)
    task_description = models.TextField(max_length=5000, blank=True)
    time_estimate = models.TimeField("Time estimate", blank=True, null=True)
    time_spent = models.TimeField("Time spent", blank=True, null=True)
    user_task = models.ForeignKey('scheduler_app.CustomUser', on_delete = models.CASCADE, related_name='user_task')
    team_task = models.ForeignKey('scheduler_teams.CustomTeam', on_delete = models.CASCADE, related_name='team_task')
    
    class Meta:
        verbose_name_plural = "Tasks"
        db_table = 'tasks'
    

    def __str__(self):
        return self.task_name


class TasksComments(models.Model):
    task_comment = models.TextField(max_length=2000, blank=True)
    task = models.ForeignKey('scheduler_tasks.Tasks', on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey('scheduler_app.CustomUser', on_delete=models.CASCADE, related_name='user_comment')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"
        db_table = "user_comments"

    def __str__(self):
        return self.task_comment