from django.urls import path
from django.contrib.auth import views as auth_views
from .forms.LoginForm import LoginForm

import sys 

sys.path.append('/Users/alexissoltysiak/Documents/GitHub/ERPsim-helper/django_server/erpsim_helper')

from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    
    path('contact/tipactualisation/<int:question_id>/', views.tip, name='tip'),

    path('contact/', views.contact, name='contact'),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='forms/login.html',
        authentication_form=LoginForm
    )),

    path('game/<int:game_id>', views.game, name="game"),


]