from django.db import models
from django.contrib.auth.models import User
from .tasks import get_game_latest_data

import datetime

# Create your models here.

class Game(models.Model):
    odata_flow = models.CharField(max_length=100)
    game_set = models.IntegerField(null=False)
    team = models.CharField(max_length=26)
    creation_date = models.DateTimeField('creation date')
    is_running = models.BooleanField(default=True, verbose_name='Running')
    is_stopped = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        #get_game_latest_data(self.id, self.odata_flow, self.game_set, self.team)
        
    def __str__(self):
        return f"Game : {str(self.id).rjust(3, '0')} - {datetime.datetime.strptime(str(self.creation_date), '%Y-%m-%d %H:%M:%S+00:00').strftime('%d/%m/%Y %H:%M')}"

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game_id = models.IntegerField()

class CompanyValuation(models.Model):
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
