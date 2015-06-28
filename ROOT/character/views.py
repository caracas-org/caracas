from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth # login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("character:login"))

    return render(request, "index.html")

def overview(request):
    return render(request, "overview.html")

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
