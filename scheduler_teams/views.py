import datetime
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from django.db.models import Prefetch
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from scheduler_teams.serializers import (
    TeamSerializer,
    GetAllUsersSerializer,
    InviteUrlSerializer,
    WorkSheetSerializer,
    GetWorkSheetSerializer
)
from scheduler_teams.models import CustomTeam, Atable
from scheduler_app.models import CustomUser
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist


class CreateTeamView(generics.GenericAPIView):
    '''
    CreateTeamView creates new team with given name
    and automatically adds creator to that team
    Response: -successful message upon creating and team_id for further redirection
              -error message if team_name already exists
    '''
    permission_classes = ((IsAuthenticated,))
    serializer_class = TeamSerializer
 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"error": "error occured"})
        team_name = request.data['team_name']
        user = request.user
        user.is_team_creator = True
        team_obj = CustomTeam(
            team_name=team_name,
        )
        team_obj.save()
        user.teams.add(team_obj)
        return Response({"message": "team created successfuly", "team_id": team_obj.id}, status=HTTP_201_CREATED)


class UpdateTeamView(generics.GenericAPIView):
    '''
    UpdateTeamView updates team name with new given team name
    Validation error occurs if team name already exist
    '''
    serializer_class = TeamSerializer
    permission_classes = ((IsAuthenticated,))

    #UpdateAPIView could be used but this is more explicit
    def put(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"error": "error occured"})
        team_name = request.data['team_name']
        team_id = kwargs['team_id']
        user = request.user
        team_obj = CustomTeam(
            id=team_id,
            team_name=team_name
        )
        team_obj.save()
        return Response({"team name changed to": team_obj.team_name}, status=HTTP_200_OK)
        

    
class GetTeamMembersView(generics.ListAPIView):
    '''
    GetTeamMembersView returns users who have same team_id
    given the keyword argument from URL
    '''
    permission_classes = ((IsAuthenticated,))
    serializer_class = GetAllUsersSerializer

    # optimization may be required
    def get_queryset(self):
        team = self.kwargs['members']
        user = self.request.user
        team_names = user.teams.all()
        team_ids = list()
        for i in team_names:
            team_ids.append(i.id)
        if team not in team_ids:
            raise PermissionDenied("Sorry, did you lost your crew?")
        users = CustomUser.objects.filter(teams=team).prefetch_related(Prefetch('atable_user', queryset=Atable.objects.filter(team=team),)) 
        return users

class GetTeamsView(generics.ListAPIView):
    '''
    GetTeamsView returns all teams for current logged-in user
    '''
    serializer_class = TeamSerializer
    permission_classes = ((IsAuthenticated,))

    def get_queryset(self):
        user = self.request.user
        teams = user.teams.all()
        return teams


class GetTeamView(generics.GenericAPIView):
    '''
    GetTeamView returns team the user is currently in
    '''
    serializer_class = TeamSerializer
    permission_classes = ((IsAuthenticated,))

    def get(self, request, team_id):
        user = request.user
        team = CustomTeam.objects.get(id=team_id)
        return Response({"team id": team.id, "team name": team.team_name})


class CreateWorkingHoursView(generics.GenericAPIView):
    '''
    PostWorkingHoursView posts new start-end time for
    user in team they're currently in
    Response: start time, end time, username, user_id, team_id
              validation error if time input is incorrect
    '''
    serializer_class = WorkSheetSerializer
    permission_classes = ((IsAuthenticated,))

    #Todo: Make Check if POST request is within already existing time range, ask for PUT
    #IF NOT, just POST another time user requested
    #How efficient is this approach?
    def post(self, request, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        user = request.user
        start_time = request.data['start_time'] # get start_time from request
        end_time = request.data['end_time'] # get end_time from request
        print(start_time, end_time)
        team_id = kwargs['team_id'] # get team_id based on current url id
        team = CustomTeam.objects.get(id=team_id) # instance of CustomTeam
        if team not in request.user.teams.all():
            raise PermissionDenied("You can't add time here")
        Atable.objects.create(user=request.user, team=team, start_time=start_time, end_time=end_time) # finally create dates
        return Response({"username": user.username, "user_id": user.id, "team_id": team.id, "start_time": start_time, "end_time": end_time}, status=HTTP_201_CREATED)


class UpdateWorkingHoursView(generics.GenericAPIView):
    '''
    UpdateWorkingHoursView updates existing start-end time for
    user in team they're currently in
    Response: start time, end time, username, user_id, team_id
              validation error if time input is incorrect
    '''
    serializer_class = WorkSheetSerializer
    permission_classes = ((IsAuthenticated,))

    def put(self, request, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        user = request.user
        start_time = request.data['start_time'] # get start_time from request
        end_time = request.data['end_time'] # get end_time from request
        print(start_time, end_time)
        atable_id = kwargs['atable_id'] # get atable_id based on current url id
        team_id = kwargs['team_id'] # get team_id based on current url id
        team = CustomTeam.objects.get(id=team_id)
        updated_time = Atable(id=atable_id, user=request.user, team=team ,start_time=start_time, end_time=end_time)
        updated_time.save()
        return Response({"username": user.username, "user_id": user.id, "team_id": team_id, "start_time": start_time, "end_time": end_time}, status=HTTP_201_CREATED)


class RemoveWorkingHoursView(generics.DestroyAPIView):
    '''
    RemoveWorkingHoursView simply removes atable time given 
    the atable_id as url param
    '''
    serializer_class = WorkSheetSerializer
    permission_classes = ((IsAuthenticated,))

    #additional checks may be required
    def destroy(self, request, **kwargs):
        atable_id = kwargs['atable_id']
        atable = Atable.objects.get(id=atable_id)
        self.perform_destroy(atable)
        return Response({"removed time": atable_id})


class GenerateURLView(generics.GenericAPIView):
    '''
    GenerateURLView creates random 7 character string and appends
    it to the current host
    Response: random invitation string
    '''
    permission_classes = ((IsAuthenticated,))
    serializer_class = InviteUrlSerializer

    def get(self, request, team_id):
        team = CustomTeam.objects.get(id=team_id)
        unique_url = get_random_string(length=7)
        team.invite_url = unique_url
        team.save()
        return Response({"url": unique_url}, status=HTTP_201_CREATED)
        

class GetUpdateTeam(generics.GenericAPIView):
    '''
    GetUpdateTeam provides user an access to the team
    where URL invitation link came from
    Response: invite_url if user is_anonymous 
              successful message upon joining
    '''
    permission_classes = [AllowAny]
    serializer_class = InviteUrlSerializer

    def get(self, request,**kwargs):
        user_obj = request.user
        invite_url = kwargs['invite_url']
        try:
            team_id = CustomTeam.objects.get(invite_url=invite_url)
        except ObjectDoesNotExist:
            return Response({'error': 'url not valid'}, status=HTTP_400_BAD_REQUEST)
        if request.user.is_anonymous:
            return Response({'register first': team_id.invite_url}, status=HTTP_401_UNAUTHORIZED)
        teams = user_obj.teams.all()
        if team_id in teams:
            return Response({"error": "user already exist in the team ", 'id': team_id.id}, status=HTTP_200_OK)
        user_obj.teams.add(team_id)
        return Response({'user added to the team': team_id.invite_url, 'id': team_id.id}, status=HTTP_200_OK)

class LeaveTeam(generics.GenericAPIView):
    '''
    LeaveTeam class provides deleting current user
    from the team 
    Response: success upon leaving 
              error if error occurs
    '''
    
    permission_classes = ((IsAuthenticated,))
    serializer_class = TeamSerializer

    def get(self, request, **kwargs):
        user = request.user
        user_id = request.user.id
        team_id = kwargs['team_id']
        current_team = CustomTeam.objects.get(id=team_id)
        try:
            user.teams.remove(current_team)
            return Response({"success": "You've successfuly left your crew"})
        except:
            return Response({'error': 'whooops, error occured!'})

class GetTeamURL(generics.GenericAPIView):
    '''
    GetTeamURL class provides invite_url endpoint
    for permanent storing on client-side
    '''

    permission_classes = ((IsAuthenticated,))
    serializer_class = InviteUrlSerializer

    def get(self, request, **kwargs):
        team_id = kwargs['team_id'] 
        team = CustomTeam.objects.get(id=team_id)
        return Response({"current url": team.invite_url})


#This class is for testing and will be removed
class ListURLView(generics.ListAPIView):
    serializer_class = InviteUrlSerializer
    queryset = CustomTeam.objects.all()