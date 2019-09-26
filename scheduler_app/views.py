from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from scheduler_app.serializers import (
    UserCreateSerializer,
    GetAllUsersSerializer,
    UserProfileSerializer,
)
from scheduler_app.models import CustomUser
from scheduler_teams.models import CustomTeam

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class GetAllUsersView(generics.ListAPIView):
    # permission_classes = ((IsAuthenticated,))
    serializer_class = GetAllUsersSerializer
    queryset = CustomUser.objects.all()


class GetCurrentUser(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id' 

    def get_queryset(self):
        return self.queryset.filter(id__exact=self.request.user.id)