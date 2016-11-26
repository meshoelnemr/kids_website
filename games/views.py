from django.shortcuts import render
from Profile.views import verified
from .models import Game, Score
from django.core.exceptions import ObjectDoesNotExist
from random import randint


@verified
def games(request):
    allgames = Game.objects.all()
    return render(request, 'games/games.html', {'games': allgames})


@verified
def math(request):
    user = request.user
    game_name = 'Math game'
    game = Game.objects.get(name=game_name)

    context = {}

    try:
        score = user.score_set.get(game=game)
    except ObjectDoesNotExist:
        score = Score(user=user, game=game)
        score.save()

    context['game']  = game
    context['score'] = score

    if request.method == 'POST':
        operation = request.POST.get('operator')
        print(operation)
        if operation == request.session['operator']:
            score.value += 1
            score.save()
            context['success'] = True
        else:
            context['failure'] = True

    # Generate new values
    val1 = randint(1, 50)
    val2 = randint(1, 50)

    operation = randint(0, 2)

    if operation == 0:
        request.session['operator'] = '+'
        result = val1 + val2
    elif operation == 1:
        if val1 < val2:
            val1, val2 = val2, val1

        request.session['operator'] = '-'
        result = val1 - val2
    else:
        request.session['operator'] = '*'
        result = val1 * val2

    context['val1'] = val1
    context['val2'] = val2
    context['result'] = result

    return render(request, 'games/math.html', context)

# def default(game_name):
#     def decorator(func):
#         @wraps(func)
#         def inner(request, *args, **kwargs):
#             user = request.user
#             game = Game.objects.get(name=game_name)
#
#             try:
#                 score = user.score_set.get(game=game)
#             except ObjectDoesNotExist:
#                 score = Score(user=user, game=game)
#                 score.save()
#
#             result = func(request, *args, **kwargs)
#
#             return render(request, 'games/%s.html' % game_name, {
#                 'game': game,
#                 'score': score,
#             })
#         return inner
#     return decorator
#
#
# @verified
# @default('Math game')
# def math(request):
#     return 'Hola'