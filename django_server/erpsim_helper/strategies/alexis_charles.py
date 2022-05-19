from datetime import datetime
from dis import Instruction
import mysql.connector
import pandas as pd
import os
from math import floor
# from django.shortcuts import render, redirect
# from django.forms import ModelForm, Textarea
# from django import forms
# from django.urls import reverse
# from django.http import HttpResponse
# from django.contrib import messages
from collections import defaultdict
import sys 

#######################################
# Find the matrice
#######################################

def trouverParametres(df,sales_organization,Materials,Localisations,precision=80):

    #Affichage
    print("Les parametres tendent vers : ")
    print(" ")

    ListeSalesJoueur = {}
    df=df[df["sales_organization"]==sales_organization]

    #Iteration Matériaux et Localisation
    for material in Materials:
        tmp=[]
        dfSalesJoueurMaterial = df[df['material_label']==material]
        for localisation in Localisations:
            if len(dfSalesJoueurMaterial[dfSalesJoueurMaterial["area"]==localisation]["quantity"])==0:
                tmp.append(0)
            else:
                tmp.append(round(dfSalesJoueurMaterial[dfSalesJoueurMaterial["area"]==localisation]["quantity"].sum()/precision,0))
        ListeSalesJoueur[material]=tmp
    print(ListeSalesJoueur)

    return ListeSalesJoueur



def prediction(sales, company, products, locations=["North","South","West"]):

    dfSales = pd.DataFrame(list(sales.values()))

    findParameters = trouverParametres(dfSales,company,products,locations)

    return findParameters

def getReapro(materials):

    reapro = {}

    reaproMilk = 900
    reaproCream = 300
    reaproYoghurt = 700
    reaproCheese = 350
    reaproButter = 400
    reaproIceCream = 300

    reapro[materials[0]]=reaproMilk
    reapro[materials[1]]=reaproCream
    reapro[materials[2]]=reaproYoghurt
    reapro[materials[3]]=reaproCheese
    reapro[materials[4]]=reaproButter
    reapro[materials[5]]=reaproIceCream

    return reapro

def getMatriceStock(prediction, materials, stock_actuel, equipe, jour_du_cycle):

    reapro=getReapro(materials)

    #if jour_du_cycle != 1:
    #  return 0

    matrice_stock={}

    for element in materials:

        somme_coef = prediction[element][0] + prediction[element][1] + prediction[element][2]
        #Dispatch du produit "element" dans les 3 entrepots
        dispatch_element=[]
        for i in range (0,3):
            dispatch_theorique = prediction[element][i] / somme_coef
            if (dispatch_theorique * reapro[element] > stock_actuel[element][i]):
                dispatch_element.append(floor(dispatch_theorique * reapro[element] - stock_actuel[element][i]))
            else:
                dispatch_element.append(0)

        #Unites non reparties dans les entrepots secondaires
        reste = reapro[element] - dispatch_element[0] - dispatch_element[1] - dispatch_element[2]

        matrice_stock[element]=[dispatch_element[0]+floor(reste/3),dispatch_element[1]+floor(reste/3),dispatch_element[2]+floor(reste/3)]

    print("matrice_stock ",matrice_stock)
  
    return(matrice_stock)

def getMatricePrix(ventes_veille, prix_actuels, frequence_reapro, jour_du_cycle, stock_actuel, materials):
    jours_cycle_restants = frequence_reapro + 1 - jour_du_cycle

    dictionnaire_prix = {}

    for element in materials:
        if (ventes_veille[element][0] >= stock_actuel[element][0]/jours_cycle_restants or ventes_veille[element][1] >= stock_actuel[element][1]/jours_cycle_restants or ventes_veille[element][2] >= stock_actuel[element][2]/jours_cycle_restants):
            dictionnaire_prix[element]=[1.1, round(1.1*prix_actuels[element], 2)]
        elif (ventes_veille[element][0] < 0.8*stock_actuel[element][0]/jours_cycle_restants and ventes_veille[element][1] < 0.8*stock_actuel[element][1]/jours_cycle_restants and ventes_veille[element][2] < 0.8*stock_actuel[element][2]/jours_cycle_restants):
            dictionnaire_prix[element]=[0.9, round(0.9*prix_actuels[element], 2)]
        else:
            dictionnaire_prix[element]=[1, round(prix_actuels[element], 2)]

    #insertDB(dictionnaire_prix, var.mydb)

    return dictionnaire_prix