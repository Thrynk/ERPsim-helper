from django.urls import path
from django.contrib.auth import views as auth_views
from .forms.LoginForm import LoginForm

from . import views

urlpatterns = [ # te
    path('', views.index, name='index'),
    path('strategy_test', views.strategy_test, name="strategy_test"),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='forms/login.html',
        authentication_form=LoginForm
    )),
    path('game/<int:game_id>', views.game, name="game"),
]