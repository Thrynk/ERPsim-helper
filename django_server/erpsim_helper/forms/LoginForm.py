from django.contrib.auth.forms import AuthenticationForm
from django.forms import IntegerField

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    gameNumber = IntegerField() # TODO: Implement choices with existing games