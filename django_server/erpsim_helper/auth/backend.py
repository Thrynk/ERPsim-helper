from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from requests import Session
from pyodata import Client
from pyodata.exceptions import HttpError
from django.utils.datastructures import MultiValueDictKeyError
from ..models import Game, Player

class ODataAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print(request)
        # retrieve game to get odata uri to test authentication
        try:
            game_id = int(request.POST["gameNumber"])
            game = Game.objects.get(pk=game_id)
        except MultiValueDictKeyError:
            return None
        
        session = Session()
        session.auth = (username, password)
        try:
            odata_service = Client(game.odata_flow, session)

            # login success, return User
            try :
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username, '', password)
            
            # create player to know which game is associated with the player
            # no need to check if player exists because on second login, default django backend will be used
            player = Player(user=user, game_id=game_id)
            player.save()
            return user
        except HttpError:
            # login failed, incorrect odata credentials
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None