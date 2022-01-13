from django.db import models
from .tasks import count_beans

# Create your models here.

class Game(models.Model):
    odata_flow = models.CharField(max_length=100)
    game_set = models.IntegerField(null=False)
    team = models.CharField(max_length=26)
    creation_date = models.DateTimeField('creation date')

    def save(self, *args, **kwargs):
        count_beans(2)
        super(Game, self).save(*args, **kwargs)