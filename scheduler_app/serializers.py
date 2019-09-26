from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from scheduler_app.models import CustomUser
from scheduler_teams.models import CustomTeam
from scheduler_teams.serializers import GetAllUsersSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    # Method for hashing password and storing user properly
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = CustomUser(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')