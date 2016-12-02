from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from Profile.views import verified
from .models import Game, Score
from random import randint, shuffle


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

    context['game'] = game
    context['score'] = score

    if request.method == 'POST':
        result = request.POST.get('answer')
        print(repr(result))
        print(repr(request.session['answer']))
        if result == request.session['answer']:
            score.value += 1
            score.save()
            context['success'] = True
        else:
            context['failure'] = True

    # Generate new values
    con, result = generate_math()
    request.session['answer'] = str(result)

    context.update(con)
    context.update(game.score_set.all().aggregate(Max('value')))
    return render(request, 'games/math.html', context)


def generate_math():
    context = {}

    val1 = randint(1, 20)
    val2 = randint(1, 20)

    operation = randint(0, 2)

    if operation == 0:
        context['operator'] = '+'
        val3 = val1 + val2
    elif operation == 1:
        if val1 < val2:
            val1, val2 = val2, val1
        context['operator'] = '-'
        val3 = val1 - val2
    else:
        context['operator'] = 'x'
        val3 = val1 * val2

    context['val1'] = val1
    context['val3'] = val3

    # generate false answers
    l = [randint(1, 20), randint(1, 20)]
    while val2 in l or l[0] == l[1]:
        if l[0] == val2:
            l[0] = randint(1, 20)
        elif l[1] == val2:
            l[1] = randint(1, 20)
        else:
            l[0] = randint(1, 20)

    l += [val2]
    shuffle(l)

    context['ans1'], context['ans2'], context['ans3'] = l

    return context, val2


@verified
def high_scores(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    # Top 50
    scores = game.score_set.order_by('-value')[:50]
    return render(request, 'games/highscores.html', {'game': game, 'scores': scores})
