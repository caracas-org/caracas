from character.models import Character
from .models import Achievement, APIUser, AchievementUnlocked
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext, loader
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse


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
        serializer = ProgressSerializer(data=request.data)
        if serializer.is_valid():
            response = dict()
            achievement = Achievement.objects.get(id=serializer.validated_data['achievement_id'])
            achievement_unlocked, created = AchievementUnlocked.objects.get_or_create(
                achievement=achievement,
                character__user_id=serializer.validated_data['user_id'],
                defaults={
                    'achievement': achievement,
                    'character': Character.objects.get(user=serializer.validated_data['user_id'])
                })
            # get or create
            # if created:
            #    print("new Achievement entry")
            response['fulfilled'] = (achievement.max_progress == achievement_unlocked.progress)
            if 'fulfilled' in serializer.data:
                response['fulfilled'] = True
            response['achievement_id'] = achievement.id
            response['achievement_image'] = achievement.icon.url if achievement.icon else ''
            response['achievement_name'] = achievement.name
            response['achievement_max_progress'] = achievement.max_progress
            response['xp_gained'] = 0 if not response['fulfilled'] else achievement.XP_gained
            if not response['fulfilled']:
                response['progress'] = min(serializer.validated_data['progress'], achievement.max_progress)
                if achievement_unlocked.progress > serializer.validated_data['progress']:
                    raise ValueError("Progress must be larger than current progress")
                if response['progress'] > achievement_unlocked.progress:
                    achievement_unlocked.progress = response['progress']
                    if response['progress'] >= achievement.max_progress:
                        response['fulfilled'] = True
                        achievement_unlocked.fulfilled = True
                        response['xp_gained'] = achievement.XP_gained
                        c = Character.objects.get(user=serializer.validated_data['user_id'])
                        c.XP += achievement.XP_gained
                        level_requirement = sum(range(c.level))*500
                        c.level = c.XP // level_requirement
                        c.save()
                    achievement_unlocked.save()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAchievements(APIView):
    """
    Retrieve achievements for a certain area.

    Send in lat/lon (as floats) and a box radius to get all achievements in the area `[lat-br, lat+br]` and
    `[lon-br, lon+br]`.

    Returns a list of Achievement objects. Each object contains all Achievement data (and stuff) as well as all the
    progress data for the currently logged-in user.
    """

    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        radius = request.GET.get('box_radius')
        if lat is None or lon is None or radius is None:
            return Response({'msg': 'send `lat`, `lon` and `box_radius`'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)
        except ValueError:
            return Response({'msg': 'send `lat`, `lon` and `box_radius` as numbers'}, status=status.HTTP_400_BAD_REQUEST)

        res = []
        for a in Achievement.objects.filter(
            lat__isnull=False, lon__isnull=False,
            lat__gte=lat-radius, lat__lte=lat+radius,
            lon__gte=lon-radius, lon__lte=lon+radius,
        ):
            a_j = {
                'achievement_id': a.id,
                'achievement_image': a.icon.url if a.icon else settings.DEFAULT_ACHIEVEMENT_IMAGE,
                'achievement_name': a.name,
                'achievement_description': a.description,
                'achievement_max_progress': a.max_progress,
                'achievement_lat': a.lat,
                'achievement_lon': a.lon,
            }
            a_unlocked_q = AchievementUnlocked.objects.filter(achievement=a, character__user=request.user)
            if a_unlocked_q:
                a_u = a_unlocked_q[0]
                a_j['progress'] = a_u.progress
                a_j['fulfilled'] = a_u.unlocked is not None
                a_j['unlocked'] = a_u.unlocked

            res.append(a_j)

        return Response({'achievements': res})

def embed(request):
    return render(request, 'api/embed.html')
    html = '''
    '''
    return HttpResponse(html)

def listAll(request):
    """
    Retrieve all achievements available and return as rendered HTML


    """
    template = loader.get_template("all_achievements.html")
    achievements = list()
    no_users = Character.objects.all().count()
    for a in Achievement.objects.all():
        total_unlocked = AchievementUnlocked.objects.filter(achievement=a).count()
        item = {
            'image_url': a.icon.url,
            'achievement_description': a.description,
            'achievement_name': a.name,
            'achievement_unlocked_total': total_unlocked,
            'user_total': no_users,
        }
        au = AchievementUnlocked.objects.get(achievement=a, character__user=request.user)
        if au:
            if au.unlocked is not None:
                item['is_unlocked'] = True
                item['unlock_date'] = au.unlocked
        achievements.append(item)

    context = RequestContext(request, {
        'achievements': achievements
    })
    return HttpResponse(template.render(context))

def recentAchievements(request):
    template = loader.get_template("recent_achievements.html")
    achievements = list()
    for a in AchievementUnlocked.objects.filter(character__user=request.user).order_by('-unlocked')[:5]:
        item = {
            'image_url': a.achievement.icon.url,
            'achievement_description': a.achievement.description,
            'achievement_name': a.achievement.name,
            'unlock_date': a.unlocked
        }
        achievements.append(item)

    context = RequestContext(request, {
        'achievements': achievements
    })
    return HttpResponse(template.render(context))
