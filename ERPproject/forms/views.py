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
    mydb = utils.dbConnexion()
    df_sales = utils.createDf(mydb, "sales")

    # Suppression des colonnes inutiles
    df_sales.drop(["sales_order_number", "line_item", "region", "city", "country", "postal_code",
                   "distribution_channel", "material_number", "material_description", "material_type",
                   "quantity_delivered", "unit", "currency"], axis=1, inplace=True)

    # Conversion des types
    columns_type = {'id_sales': 'string', 'sales_organization': 'string', 'storage_location': 'string',
                    'material_code': 'string', 'material_label': 'string', 'net_price': 'float64',
                    'net_value': 'float64', 'cost': 'float64', 'contribution_margin': 'float64',
                    'contribution_margin_pct': 'float64', 'area': 'category'}

    df_sales = df_sales.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_sales["sim_calendar_date"] = pd.to_datetime(df_sales["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_sales.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    df_group_sales_evo, graph_sales_evo = drawFigures.drawSalesEvolution(df_sales, "C9", ["Cream", "Ice Cream",
                                                                                          "Butter", "Milk", "Cheese",
                                                                                          "Yoghurt"])
    df_group_storages, graph_storages = drawFigures.drawSalesDistribution(df_sales, "C9", ["Cream", "Ice Cream",
                                                                                           "Butter", "Milk", "Cheese",
                                                                                           "Yoghurt"])

    df_inventory = utils.createDf(mydb, "inventory")

    # Suppression des colonnes inutiles
    df_inventory.drop(["material_number", "material_description", "material_type", "material_code", "unit"], axis=1,
                      inplace=True)

    # Conversion des types
    columns_type = {'id_inventory': 'string', 'plant': 'string', 'storage_location': 'string',
                    'material_label': 'string'}

    df_inventory = df_inventory.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_inventory["sim_calendar_date"] = pd.to_datetime(df_inventory["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_inventory.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    general, nord, sud, ouest, graph_inventory = drawFigures.drawStocks(df_inventory, "C9", ["Cream", "Ice Cream",
                                                                                             "Butter", "Milk",
                                                                                             "Cheese", "Yoghurt"])

    context = {
        'graph_sales_evo': graph_sales_evo,
        'graph_storages': graph_storages,
        'graph_inventory': graph_inventory
    }

    return render(request, 'detail.html', context=context)
