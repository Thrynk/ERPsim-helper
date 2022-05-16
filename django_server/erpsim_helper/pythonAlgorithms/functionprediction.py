import mysql.connector
import pandas as pd
import os
from django.shortcuts import render, redirect
from django.forms import ModelForm, Textarea
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from collections import defaultdict
import sys 

sys.path.append('/Users/alexissoltysiak/Documents/GitHub/ERPsim-helper/django_server/erpsim_helper/pythonAlgorithms')

import variables as var

 




#######################################
# Parameters
#######################################

#######################################
# Cursor
#######################################

#Function to transform a cursor to a dataframe
def cursorToCsv(cursor,cursorName):
  liste =[]
  column = []
  for x in cursor:
    liste.append(x)
  for y in cursorName:
    column.append(y[0])
  df = pd.DataFrame(liste,columns=column)
  return df


def createDf(mydb,table):
  #Creation du cursor qui va pointer vers la collection
  Cursor = mydb.cursor(buffered=True)
  Cursor.execute("USE erpsim_games_flux")
  cmd = str("SELECT * FROM "+table)
  Cursor.execute(cmd)

  CursorName = mydb.cursor()
  CursorName.execute("USE erpsim_games_flux")
  cmd = str("SELECT column_name FROM information_schema.columns WHERE table_schema='erpsim_games_flux' AND table_name='"+table+"'")
  CursorName.execute(cmd)

  df = cursorToCsv(Cursor,CursorName)
  return df

def test(db , company):
    Cursor = db.cursor()
    Cursor.execute("USE erpsim_games_flux")
    cmd = str("SELECT MAX(sim_round) FROM company_valuation WHERE company_code = '"+company+"'")
    Cursor.execute(cmd)
    rnd = list(Cursor)[0][0]
    Cursor.close()

    if rnd :

        Cursor2 = db.cursor()
        Cursor2.execute("USE erpsim_games_flux")
        cmd = str("SELECT MAX(sim_step)  FROM company_valuation WHERE company_code = '"+company+"'" + " AND sim_round = "+ str(rnd))
        Cursor2.execute(cmd)
        jour= list(Cursor2)[0][0]

        return rnd,jour
    else :
        return 0,0
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





def prediction(request):
    #Connection a la BDD SQL
    mydb = var.mydb

    #Creation des parametres en INPUT
    joueur = var.joueur
    set = var.set

    Materials = var.Materials
    Localisations = var.Localisations
    LocalisationsInventaire = var.LocalisationsInventaire

    #Donner une approximation des parametres
    dfSales = createDf(var.mydb,"sales")
    """dfInventory = createDf(mydb,"inventory")"""
    os.system('clear')

    company = str(joueur+set)

    rounds, jours = test(var.mydb,company)
    print("Round : ",rounds,"   Jour : ",jours)
    print("")

    return trouverParametres(dfSales,company,Materials,Localisations)

def materialDef():
    return ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]

def modificationPrix():

  Materials = ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]
  #Calcul du prix fonction du stock

  reaproMilk = 900
  reaproCream = 300
  reaproYoghurt = 700
  reaproCheese = 350
  reaproButter = 400
  reaproIceCream = 300

  joueur = "L"
  set = "9"

  company = str(joueur+set)


  quantiteReapro = [reaproMilk, reaproCream, reaproYoghurt, reaproCheese, reaproButter, reaproIceCream]
  frequenceReapro = 5
  ventes     = [170,60,150,65,40,50]


  df = createDf(var.mydb,"pricing_conditions")

  df=df[df["sales_organization"]==company]


  coefficients = []
  ListeReaproJoueur = {}

  for i in range (0,len(quantiteReapro)):

    if (ventes[i]>=quantiteReapro[i]/frequenceReapro):

      coefficients.append(1.05)
    elif (ventes[i]<0.8*quantiteReapro[i]/frequenceReapro):
      coefficients.append(0.95)
    else:
      coefficients.append(1)

  matriceCurrentPrices=[]

  for materials in Materials:
    dfPricingConditionMaterial = df[df['material_description']==materials]
    matriceCurrentPrices.append(dfPricingConditionMaterial['price'].iloc[-1])


  for i in range (0,6):
    valeur = [coefficients[i], round(matriceCurrentPrices[i]*coefficients[i],2)]
    ListeReaproJoueur[Materials[i]]=valeur

  return ListeReaproJoueur