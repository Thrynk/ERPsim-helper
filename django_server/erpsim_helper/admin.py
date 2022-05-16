from datetime import datetime, timedelta, date, time
import imp
import dateutil, datetime, pytz
from django.contrib import admin
from django.shortcuts import redirect

# Register your models here.
from .models import CompanyValuation, Game

# Import tasks to pause
from .tasks import store_table

class GameAdmin(admin.ModelAdmin):
    # A template for a very customized change view:
    change_form_template = 'admin/change_form.html'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("odata_flow", "game_set", "team", "creation_date", "is_running")
        return self.readonly_fields

    def get_exclude(self, request, obj=None):
        if obj is None :
            return ("is_running",)
        return self.exclude

    #def response_add(self, request, game, post_url_continue=None):
        #return redirect(f'/helper/game/{game.id}')

    def add_view(self, request, form_url='', extra_context=None):
        # Change the context in order to show or not specifics buttons
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        game = Game.objects.get(pk=object_id)

        # Check if the game is finished 
        # The game is finished if we reach sim_elapsed_steps = 80 (8 rounds with 10 days = 8 * 10 = 80 days in total)...
        # ... company_valuation is a table that contains value for every steps and it contains field sim_elapsed_steps.
        company_valuation = CompanyValuation.objects.filter(id_game = object_id).order_by('-sim_elapsed_steps').first()
        if company_valuation is not None and company_valuation.sim_elapsed_steps >= 80 : 
            print("Round >= 80")
            # To change is_running field of object_id in bdd
            game.is_stopped=True 
            game.is_running=False 
            game.save()

        # Otherwise, we consider that the game is finished if it was launched more than 1 week earlier...
        # ... we have to check the creation_date field into erpsim_helper_game table.
        _1SEMAINE = timedelta(days=7)
        current_date = datetime.datetime.now()
        current_date = pytz.utc.localize(current_date)
        if game.creation_date + _1SEMAINE < current_date and game.is_stopped == False: 
            game.is_stopped=True 
            game.is_running=False 
            game.save()

        # Check if a button has been pressed, stop or pause or play after a pause.
        if "_pause" in request.POST:
            # store_table.revoke()
            # print(store_table.is_revoked())

            # To change is_running field of object_id in bdd
            game.is_running=False 
            game.save()

        elif "_stop" in request.POST:
            # store_table.revoke()
            # print(store_table.is_revoked())

            # To change is_stopped field of object_id in bdd
            game.is_stopped=True 
            game.is_running=False 
            game.save()

        elif "_play" in request.POST:
            # Launching the tasks

            # To change is_running field of object_id in bdd
            game.is_running=True 
            game.save()

        # Change the context in order to show or not specifics buttons
        extra_context = extra_context or {}
        extra_context["show_save"] = False
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        extra_context["is_game_running"] = game.is_running
        extra_context["is_stopped"] = game.is_stopped

        return super().change_view(request, object_id, form_url, extra_context)
        #return redirect(f'/helper/game/{object_id}')

admin.site.register(Game, GameAdmin)