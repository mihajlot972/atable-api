from django.shortcuts import render
from django.urls import path, include
from .views import (
    CreateTask,
    CreateTaskComment,
)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('createtask/<int:team_id>/', CreateTask.as_view(), name='task_create'),
    path('createcomment/<int:team_id>/<int:task_id>/', CreateTaskComment.as_view(), name='comment_crate')

]