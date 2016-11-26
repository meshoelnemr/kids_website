from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    url = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' - ' + self.game.name
