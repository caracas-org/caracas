from achievements.models import Achievement
from character.models import Character
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth # login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
from django.template import loader, RequestContext
from achievements.models import AchievementUnlocked


def index(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("character:login"))

    return render(request, "index.html", {
        'character': Character.objects.get(user=request.user)
    })

def overview(request):

    template = loader.get_template("recent_achievements.html")
    achievements = list()
    for a in AchievementUnlocked.objects.filter(character__user=request.user, unlocked__isnull=False).order_by('-unlocked')[:5]:
        item = {
            'image_url': a.achievement.icon.url if a.achievement.icon else '',
            'achievement_description': a.achievement.description,
            'achievement_name': a.achievement.name,
            'unlock_date': a.unlocked
        }
        achievements.append(item)

    context = RequestContext(request, {
        'achievements': achievements
    })
    achievement_tab = template.render(context)
    #

    template = loader.get_template("all_achievements.html")
    achievements = list()
    no_users = Character.objects.all().count()
    for a in Achievement.objects.all():
        total_unlocked = AchievementUnlocked.objects.filter(achievement=a).count()
        item = {
            'image_url': a.icon.url if a.icon else '',
            'achievement_description': a.description,
            'achievement_name': a.name,
            'achievement_unlocked_total': total_unlocked,
            'users_total': no_users,
        }
        au = AchievementUnlocked.objects.filter(achievement=a, character__user=request.user)
        if au:
            au = au[0]
            if au.unlocked is not None:
                item['is_unlocked'] = True
                item['unlock_date'] = au.unlocked
        achievements.append(item)
    context = RequestContext(request, {
        'achievements': achievements
    })
    achievement_all = template.render(context)
    return render(request, "overview.html", {
        'achievement_tab': achievement_tab,
        'achievement_all': achievement_all
    })

def login(request):
    form = AuthenticationForm(request)
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse("index"))
            else:
                message = "disabled account"
        else:
            message = "invalid login"
    return render(request, "login.html", {"error_msg": message, "form":form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

def places(request):
    return render(request, "places.html")
