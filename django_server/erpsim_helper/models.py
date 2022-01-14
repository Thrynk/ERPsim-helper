from django.db import models
from .tasks import get_game_latest_data

# Create your models here.

class Game(models.Model):
    odata_flow = models.CharField(max_length=100)
    game_set = models.IntegerField(null=False)
    team = models.CharField(max_length=26)
    creation_date = models.DateTimeField('creation date')

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        get_game_latest_data(self.id, self.odata_flow, self.game_set, self.team)