from django.shortcuts import render, redirect, reverse
from django.forms import ModelForm
from django.contrib import messages
from .models import Contact
from . import drawFigures
from . import utils
from django import forms
import pandas as pd


# Create your views here.

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('gameNumber', 'login', 'password')
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        }


def form(request):
    # on instancie un formulaire
    form_contact = ContactForm()
    # on teste si on est bien en validation de formulaire (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form_contact = ContactForm(request.POST)
        # on vérifie la validité du formulaire
        if form_contact.is_valid():
            new_contact = form_contact.save()
            messages.success(request, 'Game Number ' + new_contact.gameNumber + ' & player : ' + new_contact.login)
            context = {'pers': new_contact}
            # return redirect(reverse('detail'))
            return render(request, 'detail.html', context)
    else:
        # Si méthode GET, on présente le formulaire
        context = {'form': form_contact}
        return render(request, 'form.html', context)


def detail(request):

    import time
    now = time.time()

    mydb = utils.dbConnexion()

    now2 = time.time()
    print(f"Connexion : {now2-now} secondes")

    df_sales = utils.getSalesData(mydb)

    now3 = time.time()
    print(f"get sales df : {now3-now2} secondes")

    # Conversion des types
    columns_type = {'sales_organization': 'string', 'storage_location': 'string', 'material_label': 'string'}
    df_sales = df_sales.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_sales["sim_calendar_date"] = pd.to_datetime(df_sales["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_sales.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    now4 = time.time()
    print(f"Preprocessing sales : {now4 - now3} secondes")

    df_group_sales_evo, graph_sales_evo = drawFigures.drawSalesEvolution(df_sales, "C9", ["Cream", "Ice Cream",
                                                                                          "Butter", "Milk", "Cheese",
                                                                                          "Yoghurt"])
    df_group_storages, graph_storages = drawFigures.drawSalesDistribution(df_sales, "C9", ["Cream", "Ice Cream",
                                                                                           "Butter", "Milk", "Cheese",
                                                                                           "Yoghurt"])

    now5 = time.time()
    print(f"Generate graph sales : {now5-now4} secondes")

    df_inventory = utils.getInventoryData(mydb)
    now6 = time.time()
    print(f"get inventory df : {now6-now5} secondes")

    # Conversion des types
    columns_type = {'plant': 'string', 'storage_location': 'string', 'material_label': 'string'}
    df_inventory = df_inventory.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_inventory["sim_calendar_date"] = pd.to_datetime(df_inventory["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_inventory.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    now7 = time.time()
    print(f"Preprocessing inventory : {now7-now6} secondes")

    general, nord, sud, ouest, graph_inventory = drawFigures.drawStocks(df_inventory, "C9", ["Cream", "Ice Cream",
                                                                                             "Butter", "Milk",
                                                                                             "Cheese", "Yoghurt"])

    context = {
        'graph_sales_evo': graph_sales_evo,
        'graph_storages': graph_storages,
        'graph_inventory': graph_inventory
    }

    return render(request, 'detail.html', context=context)
