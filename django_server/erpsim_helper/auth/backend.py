from django.contrib.auth.backends import BaseBackend

from erpsim_helper.models import User
from requests import Session
from pyodata import Client
from pyodata.exceptions import HttpError
from django.utils.datastructures import MultiValueDictKeyError
from ..models import Game, Player

class ODataAuthenticationBackend(BaseBackend): #TODO: put a link to application login policy
    """
        The ODataAuthenticationBackend objects is used to handle login logic. 
        This class inherits from BaseBackend.

        ...

        Methods
        -------
        authenticate(request, username=None, password=None):
            Authenticates user according to application policy.

        get_user(user_id):
            Get user from its primary key.
    """

    def authenticate(self, request, username=None, password=None):
        """
            Authenticate the user according to login policy.

            If admin is trying to connect then check password and log in if correct.
            If a player is trying to connect:
                - And it is his first connection, then check credentials with odata flow and create user if success.
                - If it is not the first connection, then retrieve user associated with the game (via Player model) and check his password.

            :param request: Request information from browser
            :type request: WSGIRequest
            :param username: Username from login form
            :type username: str
            :param password: Password entered by user in login form
            :type password: str
        """
        
        try:
            game_id = int(request.POST["gameNumber"])
            try:
                # retrieve game to get odata uri to test authentication
                game = Game.objects.get(pk=game_id)
            except Game.DoesNotExist:
                return None
        except MultiValueDictKeyError:
            # if there is no gameNumber in form, user is trying to log from admin form
            try:
                admin = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
            if not admin.check_password(password):
                return None
            return admin

        
        try:
            # check if player is already associated with a game
            player_associated_with_game = Player.objects.get(game_id=game.id)

            # if player exists, then retrieve appropriate user
            user = User.objects.get(pk=player_associated_with_game.user_id)

            # if entered password is incorrect
            if not user.check_password(password):
                return None

            return user
        except Player.DoesNotExist:
            # if player does not exist, then test user credentials against odata
            session = Session()
            session.auth = (username, password)
            try:
                odata_service = Client(game.odata_flow, session)

                # login odata success, create user
                user = User.objects.create_user(username, '', password)
                
                # create player to know which game is associated with the player

                player = Player(user=user, game_id=game_id)
                player.save()

                return user
            except HttpError:
                # login failed, incorrect odata credentials
                return None

    def get_user(self, user_id):
        """
            Get user from id

            :param user_id: User ID
            :type user_id: str
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None