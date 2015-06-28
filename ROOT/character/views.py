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

    return render(request, "index.html")

def overview(request):

    template = loader.get_template("recent_achievements.html")
    achievements = list()
    for a in AchievementUnlocked.objects.filter(character__user=request.user, unlocked__isnull=False).order_by('-unlocked')[:5]:
        item = {
            'image_url': a.achievement.icon.url if a.achievement.icon else '',
            'achievement_decription': a.achievement.description,
            'achievement_name': a.achievement.name,
            'unlock_date': a.unlocked
        }
        achievements.append(item)

    context = RequestContext(request, {
        'achievements': achievements
    })
    achievement_tab = template.render(context)

    return render(request, "overview.html", {
        'achievement_tab': achievement_tab,
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
