import imp
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Game


def index(request):
    return HttpResponse("Hello, world. You're at the helper index.")

def game(request, game_id):
    game = Game.objects.get(pk=game_id)
    return HttpResponse(f"Game page : {game.id} \n Flux odata : {game.odata_flow}.")