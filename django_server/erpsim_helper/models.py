from django.db import models
from django.contrib.auth.models import User
from .tasks import get_game_latest_data

import datetime

# Create your models here.

class Game(models.Model):
    """
        The Game objects represents a game. 
        
        This class has all the useful fields to define a game.
        The game is composed of 
        * An odata flow - To catch the data 
        * A game set - By default in the simulator. It corresponds to different space of game
        * A team - By default in the simulator. 
        * A creation date. 
        and two indicators about the game.
        * is_running - An indictor to know if the game is running or not.
        * is_stopped - An indicator to know if the game is stopped or not.
    """
    odata_flow = models.CharField(max_length=100)
    game_set = models.IntegerField(null=False)
    team = models.CharField(max_length=26)
    creation_date = models.DateTimeField('creation date')
    is_running = models.BooleanField(default=True, verbose_name='Running')
    is_stopped = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        """
            Save a game. 

            :param *args:
            :type *args: str
            :param **kwargs: 
            :type **kwargs: list['str']
        """
        super(Game, self).save(*args, **kwargs)
        #get_game_latest_data(self.id, self.odata_flow, self.game_set, self.team)
        
    def __str__(self):
        """
            Override the `__str__(self)` method for logs
        """
        return f"Game : {str(self.id).rjust(3, '0')} - {datetime.datetime.strptime(str(self.creation_date), '%Y-%m-%d %H:%M:%S+00:00').strftime('%d/%m/%Y %H:%M')}"

class Player(models.Model):
    """
        The object Player represents a player in a team. 

        A player is playing in one game, so it is composed of `game_id`, and 
        naturally with his identity with `user.`
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game_id = models.IntegerField()

class CompanyValuation(models.Model):
    """
        The CompanyValuation object represents a table with data. 

        The company valuation is the "reward" of the company. If you're good player,
        you have a good, high company valuation. Moreover, the company valuation is calculated at 
        each day of the simulation, so that he can check the state of the game.

        All the fields of this class are defined in the simulation directly. There are all the fields given
        by the simuation.
    """
    id_company_valuation = models.BigAutoField(primary_key=True)
    row_number = models.IntegerField()
    company_code = models.CharField(max_length=2)
    sim_round = models.IntegerField()
    sim_step = models.IntegerField()
    sim_calendar_date = models.DateTimeField()
    sim_period = models.IntegerField()
    sim_elapsed_steps = models.IntegerField()
    bank_cash_account = models.FloatField()
    accounts_receivable = models.IntegerField()
    bank_loan = models.FloatField()
    accounts_payable = models.FloatField()
    profit = models.FloatField()
    debt_loading = models.FloatField()
    credit_rating = models.CharField(max_length=10)
    company_risk_rate_pct = models.FloatField()
    company_valuation = models.FloatField()
    currency = models.CharField(max_length=3)
    id_game = models.ForeignKey(Game, models.CASCADE, db_column='id_game')

    class Meta:
        managed = False
        db_table = 'company_valuation'
