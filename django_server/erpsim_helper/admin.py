import imp
from django.contrib import admin
from django.shortcuts import redirect

# Register your models here.
from .models import Game

# Import tasks to pause
from .tasks import store_table

class GameAdmin(admin.ModelAdmin):
    # A template for a very customized change view:
    change_form_template = 'admin/change_form.html'
    readonly_fields=('is_running',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("odata_flow", "game_set", "team", "creation_date")
        return self.readonly_fields

    #def response_add(self, request, game, post_url_continue=None):
        #return redirect(f'/helper/game/{game.id}')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        game = Game.objects.get(pk=object_id)

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
            game.save()

        elif "_play" in request.POST:
            # Launching the tasks

            # To change is_running field of object_id in bdd
            game.is_running=True 
            game.save()

        extra_context = extra_context or {}
        extra_context["show_save"] = False
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False
        extra_context["is_game_running"] = game.is_running
        extra_context["is_stopped"] = game.is_stopped
        return super().change_view(request, object_id, form_url, extra_context)
        #return redirect(f'/helper/game/{object_id}')

admin.site.register(Game, GameAdmin)