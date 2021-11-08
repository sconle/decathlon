import json
import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as true_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from game.models import *

@csrf_exempt
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
    gameName = request.POST.get("game-name")

    game0 = JavelinThrow(name=gameName, number_of_player=numberPlayer)
    game0.save()
    return render(request, "javelot/play.html", {"id": game0.id,
                                                 "number": numberPlayer,
                                                 "de1": game0.dice_value["1"],
                                                 "de2": game0.dice_value["2"],
                                                 "de3": game0.dice_value["3"],
                                                 "de4": game0.dice_value["4"],
                                                 "de5": game0.dice_value["5"],
                                                 "de6": game0.dice_value["6"],
                                                 "joueur": game0.currentPlayer,
                                                 "restant": game0.remaining_attempts,
                                                 })

@csrf_exempt
def roll_dice(request):
    redirect = False
    number = [1, 2, 3, 4, 5, 6]
    id = request.POST.get("id")
    number_player = request.POST.get("number")
    old_player = request.POST.get("nplayer")
    print(old_player)
    conserv = json.loads(request.POST.get("conserv"))
    game = JavelinThrow.objects.get(pk=id)
    if conserv == {} and game.dice_value != {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1}:
        sum = 0
        impair = 0
        keeped_in_if = list(game.dice_keeped.keys())
        print(list(game.dice_keeped.keys()))
        for dice in number:
            if str(dice) not in keeped_in_if:
                impair += game.dice_value[str(dice)] % 2
        if impair != 0 or len(list(game.dice_keeped.keys())) == 6:
            for dice in game.dice_keeped:
                sum += game.dice_value[str(dice)]
            game.scoreboard[game.currentPlayer] += sum
        game.dice_keeped = {}
        if int(game.currentPlayer[-1]) + 1 <= int(number_player):
            chiffre = int(game.currentPlayer[-1])
            game.currentPlayer = game.currentPlayer[:-1]
            game.currentPlayer = game.currentPlayer + str(chiffre + 1)
        else:
            game.currentPlayer = game.currentPlayer[:-1] + "1"
            if game.remaining_attempts == 1:
                redirect =True
                #return render(request, "javelot/resultat.html")
            else:
                game.remaining_attempts -= 1
    game.dice_keeped.update(conserv)
    for i in number:
        if str(i) not in game.dice_keeped:
            game.dice_value[f"{i}"] = random.randint(1, 6)

    game.save()
    keeped = list(game.dice_keeped.keys())
    message = {f"de{k}": game.dice_value[f"{k}"] for k in number}
    message.update({f"deKeeped{int(k)}": game.dice_value[f"{int(k)}"] for k in keeped})
    message.update({"joueur": game.currentPlayer,
                    "ancien_joueur": old_player,
                    "restant": game.remaining_attempts,
                    "keeped": keeped,
                    "redirect": redirect
                     })
    return JsonResponse(message)


def result(request, game_id):
    id = int(game_id)
    game = JavelinThrow.objects.get(pk=id)
    message = {"id": id, "nplayer": game.number_of_player, "nb_joueur": len(game.scoreboard.keys())}
    for i in range(1,len(game.scoreboard.keys())+1):
        message.update({f"player{i}": game.scoreboard[f"player{i}"]})
    return render(request, 'javelot/resultat.html', message)
