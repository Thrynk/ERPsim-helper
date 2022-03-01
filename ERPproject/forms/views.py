from django.shortcuts import render, redirect
from django.forms import ModelForm, Textarea
from forms.models import Contact
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('gameNumber', 'login', 'password')
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        }


from django import forms

"""class ContactForm2(forms.Form):
    
    name = forms.CharField(max_length=50, initial="Votre nom", label="nom")
    firstname = forms.CharField(max_length=50,  initial="Votre prénom", 
    label="prenom")
    email = forms.EmailField(max_length=200, label='mail')
    message = forms.CharField(max_length=1000, 
    widget=forms.Textarea(attrs={'cols':20, 'rows': 10}))
"""

""" def contact(request):
    contact_form = ContactForm()
    contact_form2 = ContactForm2()
    return render(request, 'contact.html', 
    {'contact_form': contact_form,
    'contact_form2': contact_form2  })
 """


def contact(request):
    # on instancie un formulaire
    form = ContactForm()
    # on teste si on est bien en validation de formulaire (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form = ContactForm(request.POST)
        # on vérifie la validité du formulaire
        if form.is_valid():
            new_contact = form.save()
            messages.success(request, 'Game Number ' + new_contact.gameNumber + ' & player : ' + new_contact.login)
            # return redirect(reverse('detail', args=[new_contact.pk] ))
            context = {'pers': new_contact}
            return render(request, 'detail.html', context)
    # Si méthode GET, on présente le formulaire
    context = {'form': form}
    return render(request, 'contact.html', context)


def detail(request, cid):
    contact = Contact.objects.get(pk=cid)
    return HttpResponse('Game Number : ' + contact.gameNumber + ' Player : ' + contact.login)
