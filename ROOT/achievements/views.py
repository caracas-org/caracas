from django.utils import timezone
from .models import Achievement, APIUser, AchievementUnlocked
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class ProgressSerializer(serializers.Serializer):
    achievement_id = serializers.CharField()
    auth_token = serializers.CharField()
    user_id = serializers.CharField()
    fulfilled = serializers.BooleanField()
    progress = serializers.IntegerField(required=False)

    def validate_achievement_id(self, value):
        if not Achievement.objects.filter(id=value).exists():
            raise serializers.ValidationError("Achievement ID does not exist")
        return value

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return User.objects.get(id=value)

    def validate_auth_token(self, value):
        if not APIUser.objects.filter(auth_token=value).exists():
            raise serializers.ValidationError("Auth token is not correct")
        return APIUser.objects.get(auth_token=value)

    def validate(self, data):
        api_user = data['auth_token']
        if data['fulfilled'] == False and data['progress'] == None:
            raise serializers.ValidationError("Either fulfilled or progress have to be set")
        if not api_user.achievements.filter(id=data['achievement_id']).exists():
            raise serializers.ValidationError("Not authorized to update this Achievement")
        return data


class AchievementProgressSerializer(serializers.Serializer):
    """
    The serializer for returning data after a progress/fulfill was called.
    """

    progress = serializers.IntegerField()
    fulfilled = serializers.BooleanField()
    xp_gained = serializers.IntegerField()

    achievement_id = serializers.CharField()
    achievement_image = serializers.URLField()
    achievement_name = serializers.CharField()
    achievement_max_progress = serializers.IntegerField()



class UnlockProgress(APIView):
    """
    Mark that a user made progress on an achievement or fulfilled an achievement.

    You must send a JSON object that contains these attributes:

    * `achievement_id`: The id of the achievement you want to unlock. Look this up in your documentation!
    * `auth_token`: your authentication token
    * `user_id`: The ID of the user that progressed on the achievement.
    * `progress`: The progress number of your achievement. This must be higher or equal to the current
      state of the achievement, otherwise this message will be discarded. If you send `fulfilled == true`,
      this will also be ignored.
    * `fulfilled`: boolean attribute. If you send `true`, the achievement will marked with full progress and
      marked as unlocked.

    In case your request was successful, you will get:
    * `progress`:
    * `fulfilled`:
    * `xp_gained`:
    * `achievement_id`:
    * `achievement_image`:
    * `achievement_name`:
    * `achievement_max_progress`:
    """

    serializer_class = ProgressSerializer

    def post(self, request):
        serializer = ProgressSerializer(data=request.data)
        if serializer.is_valid():
            response = dict()
            achievement = Achievement.objects.get(id=serializer.validated_data['achievement_id'])
            achievement_unlocked = AchievementUnlocked.objects.get(achievement_id=serializer.validated_data['achievement_id'], character__user_id=serializer.validated_data['user_id'])
            #get or create
            response['fulfilled'] = (achievement.max_progress == achievement_unlocked.progress)
            response['achievement_id'] = achievement.id
            response['achievement_image'] = achievement.icon.url
            response['achievement_name'] = achievement.name
            response['achievement_max_progress'] = achievement.max_progress
            response['progress'] = min(serializer.validated_data['progress'], achievement.max_progress)
            response['xp_gained'] = 0 if not response['fulfilled'] else achievement.XP_gained
            if achievement_unlocked.progress > serializer.validated_data['progress']:
                raise ValueError("Progress must be larger than current progress")
            if not response['fulfilled']:
                if response['progress'] > achievement_unlocked.progress:
                    achievement_unlocked.progress = response['progress']
                    if response['progress'] >= achievement.max_progress:
                        response['fulfilled'] = True
                        achievement_unlocked.fulfilled = True
                        response['xp_gained'] = achievement.XP_gained
                    achievement_unlocked.save()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAchievements(APIView):
    """
    Retrieve achievements for a certain area.

    Send in lat/lon (as floats) and a box radius to get all achievements in the area `[lat-br, lat+br]` and
    `[lon-br, lon+br]`.
    """

    def get(self, request):
        return Response({'not implemented': 'yet', 'achievements': []})
