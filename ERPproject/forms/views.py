from django.shortcuts import render
from django.forms import ModelForm
from forms.models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('gameNumber', 'login', 'password')


def contact(request):
    contact_form = ContactForm()
    return render(request, 'contact.html', {'contact_form': contact_form})
