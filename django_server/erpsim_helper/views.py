from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import DetailView

from .models import Game,Contact,Tips

from .tasks import get_game_latest_data
from .pythonAlgorithms.functionprediction import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('gameNumber', 'login', 'password')
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        }

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




def contact(request):
    # on instancie un formulaire
    form = ContactForm()
    # on teste si on est bien en validation de formulaire (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        #form = ContactForm(request.POST)
        # on vérifie la validité du formulair

        #if form.is_valid():

        #new_contact = form.save()
        #messages.success(request, 'Game Number ' + new_contact.gameNumber + ' & player : ' + new_contact.login)
        # return redirect(reverse('detail', args=[new_contact.pk] ))

        #context = {}
        #return render(request, 'forms/detail.html', context)


        
        #ListInstructions=get_Instructions()

        context = {'pers': "tst",'tips':getTheTipsBack(),'predictions':prediction(request),'material':materialDef,'modifPrix':modificationPrix()}

        return render(request, 'forms/detail.html', context)




    # Si méthode GET, on présente le formulaire
    context = {'form': form}
    return render(request, 'forms/detail.html', context)






class PublisherDetail(DetailView):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = "yo"
        return context


def tip (request, question_id):

    tip = Tips.objects.filter(id=question_id)
    tip.update(is_active=False)

    context = {'pers': "tst",'tips':getTheTipsBack(),'predictions':prediction(request),'material':materialDef,'modifPrix':modificationPrix()}

    return render(request, 'forms/detail.html', context)

