from django.shortcuts import render
from django.forms import Form, CharField, PasswordInput
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Game, Player
from .tasks import get_game_latest_data

# Create your views here.
class ContactForm(Form):
    """
        The ContactForm object is usefull for login. 

        To be connected with the odata flow, we have to fill : 
        * The number of the game (Game ID)
        * The login 
        * The password
    """
    gameNumber = CharField(max_length=200)
    login = CharField(max_length=200)
    password = CharField(widget=PasswordInput, max_length=200)

@login_required
def index(request):     # TO DO
    """
        Redirect if user is not logged in, else display dashboard page. 

        :param request:
        :type request: django.http.HttpRequest

        :return: Http response
        :rtype: Http response
    """
    player_associated_with_user = Player.objects.get(user=request.user.id)

    return HttpResponse(f"Hello, Player : {request.user.username}. \n Your associated game is {player_associated_with_user.game_id}.")

def game(request, game_id):     # TO DO
    """
        Get the current game. 

        :param request:
        :type request:
        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 
    """
    game = Game.objects.get(pk=game_id)
    return HttpResponse(f"Game page : {game.id} \n Flux odata : {game.odata_flow}.")