from django.conf.urls import url
from . import views

app_name = 'games'

urlpatterns = [
    # Games main page
    url(r'^$', views.games, name='games'),

    # Math game
    url(r'^math/$', views.math, name='math'),

    # English game
    url(r'^english/$', views.games, name='english'),

    # Hgih scores
    url(r'^highscores/(?P<game_id>\d+)/$', views.high_scores, name='highscores'),
]
