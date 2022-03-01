import imp
from django.contrib import admin
from django.shortcuts import redirect

# Register your models here.
from .models import Game

class GameAdmin(admin.ModelAdmin):
    def response_add(self, request, game, post_url_continue=None):
        return redirect(f'/helper/game/{game.id}')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        #return super().change_view(request, object_id, form_url, extra_context)
        return redirect(f'/helper/game/{object_id}')

admin.site.register(Game, GameAdmin)