from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class ProgressSerializer(serializers.Serializer):
    achievement_id = serializers.CharField()
    auth_token = serializers.CharField()
    user_id = serializers.CharField()
    fulfilled = serializers.BooleanField()
    progress = serializers.IntegerField(
        required=False,
    )



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
    * `progress`: The new value of the progress of this achievement for the given user.
    * `fulfilled`: Boolean, whether the achievement was fully progressed or not. If you sent `fulfilled == true`, then
      this will be true.
    * `xp_gained`: The amount of XP the user gained for getting this achievement.
    * `achievement_id`: The id of the achievement.
    * `achievement_image`: The image for this achievement as a URL that can be embedded directly in your page.
    * `achievement_name`: The (readable) name of the achievement.
    * `achievement_max_progress`: The amount of progress this achievement must do before it is fully unlocked.
    """

    serializer_class = ProgressSerializer

    def post(self, request):
        print(request.DATA)
        return Response({'not implemented': 'yet'})


class GetAchievements(APIView):
    """
    Retrieve achievements for a certain area.

    Send in lat/lon (as floats) and a box radius to get all achievements in the area `[lat-br, lat+br]` and
    `[lon-br, lon+br]`.
    """

    def get(self, request):
        return Response({'not implemented': 'yet', 'achievements': []})
