from django.shortcuts import render
from django.urls import path, include
from .views import (
    CreateTeamView,
    UpdateTeamView, 
    GetTeamMembersView,
    GenerateURLView,
    ListURLView,
    GetUpdateTeam,
    GetTeamsView,
    UpdateWorkingHoursView,
    CreateWorkingHoursView,
    LeaveTeam,
    GetTeamURL,
    GetTeamView,
    RemoveWorkingHoursView,
)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('createteam/', CreateTeamView.as_view(), name='teams_create'),
    path('createteam/<int:team_id>/update/', UpdateTeamView.as_view(), name='team_update'),
    path('list/<int:members>/', GetTeamMembersView.as_view(), name='team_members'),
    path('removetime/<int:atable_id>/', RemoveWorkingHoursView.as_view(), name='delete_time'),
    path('createurl/<int:team_id>/', GenerateURLView.as_view(), name='team_members'),
    path('updatetime/<int:team_id>/<int:atable_id>/', csrf_exempt(UpdateWorkingHoursView.as_view()), name='update_working_hours'),
    path('createtime/<int:team_id>/', CreateWorkingHoursView.as_view(), name='create_working_hours'),
    path('createurl/list/', ListURLView.as_view(), name='team_members'),
    path('jointeam/<slug:invite_url>/', GetUpdateTeam.as_view(), name='join_member'),
    path('list/', GetTeamsView.as_view(), name='user_teams'),
    path('team/<int:team_id>/', GetTeamView.as_view(), name='user_team'),
    path('leave/<int:team_id>/', LeaveTeam.as_view(), name='leave_team'),
    path('geturl/<int:team_id>/', GetTeamURL.as_view(), name='get_team_url')
]