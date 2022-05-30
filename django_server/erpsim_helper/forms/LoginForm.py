from django.contrib.auth.forms import AuthenticationForm
from django.forms import IntegerField

class LoginForm(AuthenticationForm):
    """
        This is a custom login form inherited from AuthenticationForm. We added a game number field to ask player in which game, he is going to play.
    """
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    gameNumber = IntegerField() # TODO: Implement choices with existing games