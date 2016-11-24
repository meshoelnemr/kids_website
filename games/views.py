from django.shortcuts import render
from Profile.views import verified
from .models import *


@verified
def games(request):
    all_games = Game.objects.all()
    return render(request, 'games/games.html', {'games': all_games})


@verified
def math(request):
    return render(request, 'games/math.html')
