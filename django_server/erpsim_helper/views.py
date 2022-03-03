from django.shortcuts import render
from django.forms import Form, CharField, PasswordInput
from django.http import HttpResponse
from django.contrib import messages

from .models import Game
from .tasks import get_game_latest_data

# Create your views here.
class ContactForm(Form):
    gameNumber = CharField(max_length=200)
    login = CharField(max_length=200)
    password = CharField(widget=PasswordInput, max_length=200)

def index(request):
    return HttpResponse("Hello, world. You're at the helper index.")

def game(request, game_id):
    game = Game.objects.get(pk=game_id)
    return HttpResponse(f"Game page : {game.id} \n Flux odata : {game.odata_flow}.")

def login(request):
    # on teste si on est bien en validation de formulaire (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form = ContactForm(request.POST)

        # on vérifie la validité du formulaire
        if form.is_valid():
            print(form.cleaned_data)
            new_login = form.cleaned_data
            messages.success(request, 'Game Number ' + new_login["gameNumber"] + ' & player : ' + new_login["login"])
            
            game = Game.objects.get(pk=new_login["gameNumber"])
            # get_game_latest_data(game.id, game.odata_flow, game.game_set, game.team, new_login['login'], new_login['password'])

            # return redirect(reverse('detail', args=[new_contact.pk] ))
            context = {'pers': new_login}
            return render(request, 'forms/detail.html', context)
    # Si méthode GET, on présente le formulaire
    context = {'form': form}
    return render(request, 'forms/login.html', context)