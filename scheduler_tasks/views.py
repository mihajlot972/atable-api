from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from scheduler_tasks.serializers import TaskSerializer, TaskCommentSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from scheduler_app.models import CustomUser
from scheduler_teams.models import CustomTeam
from scheduler_tasks.models import Tasks, TasksComments

# Create your views here.
class CreateTask(generics.GenericAPIView):
    '''
    CreateTaskView creates new task with task_name,
    task_description, time_estimate and time_spent
    '''

    serializer_class = TaskSerializer
    permission_classes = ((IsAuthenticated,))

    def post(self, request, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        user = request.user
        team_id = kwargs['team_id']
        task_name = request.data['task_name']
        task_description = request.data['task_description']
        team = CustomTeam.objects.get(id=team_id)
        Tasks.objects.create(user_task=user, team_task=team, task_name=task_name, task_description=task_description)
        return Response({"success": "task created successfuly"}, status=HTTP_201_CREATED)
        

class CreateTaskComment(generics.GenericAPIView):
    '''
    CreateTaskComment creates new comment within
    specific task
    '''
    
    serializer_class = TaskCommentSerializer
    permission_classes = ((IsAuthenticated,))

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        comment = request.data['task_comment']
        user = request.user
        team_id = kwargs['team_id']
        task_id = kwargs['task_id']
        team = CustomTeam.objects.get(id=team_id)
        task = Tasks.objects.get(id=task_id)
        TasksComments.objects.create(task=task, user=user, task_comment=comment)
        return Response({"comment added": "user " + str(user.id)}, status=HTTP_201_CREATED)


class RemoveTaskComment(generics.DestroyAPIView):
    '''
    RemoveTaskComment removes new comment within
    specific task
    '''
    serializer_class = TaskCommentSerializer
    permission_classes = ((IsAuthenticated,))

    def destroy(self, request, **kwargs):
        task_comment_id = kwargs['task_id']
        task = TasksComments.objects.get(id=task_comment_id)
        self.perform_destroy(task)
        return Response({"comment deleted": task_comment_id}) 