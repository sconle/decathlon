from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as true_logout

from game.models import *


def index(request):
    if request.POST.get("pseudo") is not None and str(request.POST.get("pseudo")) != "" \
            and str(request.POST.get("password")) != "":
        user = authenticate(username=request.POST.get("pseudo"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
        else:
            return render(request, "user_not_exist.html")
    if request.user.is_authenticated:
        template = "index.html"
    else:
        template = "signin.html"
    return render(request, f"{template}")


def createUser(request):
    if request.POST.get("pseudo") is not None and str(request.POST.get("pseudo")) != "" \
            and str(request.POST.get("password")) != "" and str(request.POST.get("mail")) != "":

        try:
            User.objects.get(username=request.POST.get("pseudo"))
        except:
            existUser = False
        else:
            existUser = True
        if existUser:
            return render(request, "user_exist.html")
        else:
            user = User.objects.create_user(str(request.POST.get("pseudo")),
                                            str(request.POST.get("mail")),
                                            str(request.POST.get("password")))
            login(request, user)
    return redirect('/')

def signup(request):
    return render(request, "signup.html")


def logout(request):
    true_logout(request)
    return redirect('/')


def javelot_settings(request):
    return render(request, "javelot/settings.html")


def javelot_play(request):
    numberPlayer = request.POST.get("number-player")
    return render(request, "javelot/play.html", {'nombre_de_joueur':numberPlayer})