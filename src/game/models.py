from django.db import models


def dict_scoreboard():
    return {"player1": 0,
            "player2": 0,
            "player3": 0,
            "player4": 0
            }

def dict_dice():
    return {"1": 1,
            "2": 1,
            "3": 1,
            "4": 1,
            "5": 1,
            "6": 1
            }


def dict_keeped():
    return {}


class JavelinThrow(models.Model):
    name = models.CharField(max_length=20)
    dice_value = models.JSONField(default=dict_dice())
    dice_keeped = models.JSONField(default=dict_keeped())
    currentPlayer = models.CharField(default="player1", max_length=50)
    scoreboard = models.JSONField(default=dict_scoreboard)
    remaining_attempts = models.IntegerField(default=3)
    is_online = models.BooleanField(default=True)

    def max_score(self):
        return max(self.scoreboard, key=self.scoreboard.get), \
               self.scoreboard[max(self.scoreboard, key=self.scoreboard.get)]

