from django.contrib.auth.backends import BaseBackend

from erpsim_helper.models import User
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
            # Admin is trying to log in
            admin = User.objects.get(username=username)
            if not admin.check_password(password):
                return None
            return admin

        # check if player is already associated with a game
        try:
            # if player exists, then retrieve appropriate user id
            player_associated_with_game = Player.objects.get(game_id=game.id)
            print(player_associated_with_game)

            user = User.objects.get(pk=player_associated_with_game.user_id)
            # TODO: authenticate user with password

            if not user.check_password(password):
                return None

            return user
        except Player.DoesNotExist:
            session = Session()
            session.auth = (username, password)
            try:
                odata_service = Client(game.odata_flow, session)

                # login odata success, create user
                user = User.objects.create_user(username, '', password)
                # try :
                #     user = User.objects.get(username=username)
                #     #player_associated_with_game = Player.objects.get(game_id=game.id)
                # except User.DoesNotExist:
                #     user = User.objects.create_user(username, '', password)
                
                # create player to know which game is associated with the player
                # no need to check if player exists because on second login, default django backend will be used
                print(f"user {user.id}")
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