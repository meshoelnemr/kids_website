from django.conf.urls import url
from . import views

app_name = 'games'

urlpatterns = [
    # Games main page
    url(r'^$', views.games, name='games'),

    # Math game
    url(r'^math/$', views.math, name='math')
]
