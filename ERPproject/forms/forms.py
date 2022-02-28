from django import forms


class ContactForm(forms.Form):
    gameNumber = forms.CharField(max_length=30)
    login = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        gameNumber = cleaned_data.get('gameNumber')
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if not gameNumber and not login and not password:
            raise forms.ValidationError('You have to write something!')
