from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from scheduler_teams.models import CustomTeam, Atable
from scheduler_app.models import CustomUser


# ModelSerializer turns out to be potentionally slow

class WorkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atable
        fields = ('start_time', 'end_time', 'date')

    # Validation is still not fully implemented
    def validate(self, validated_data):
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        if start_time == end_time:
            raise ValidationError({"error": "Start time and end time cannot be same"})
        # if start_time == start_time or end_time == end_time:
        #     raise ValidationError({"error": "PUT request required"})
        return validated_data


class GetWorkSheetSerializer(serializers.ModelSerializer):
    '''
    This serializer is created to get Atable view only for GET
    requests
    WorkSheetSerializer is used for POST requests
    '''
    class Meta:
        model = Atable
        fields = ('id', 'team', 'user','start_time', 'end_time', 'date')
    

class GetAllUsersSerializer(serializers.ModelSerializer):
    atable_user = GetWorkSheetSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_team_creator', 'teams', 'atable_user')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTeam
        fields = ('id', 'team_name')


class InviteUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTeam
        fields = ('id', 'invite_url',)