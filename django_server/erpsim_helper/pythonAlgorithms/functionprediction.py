from datetime import datetime
from dis import Instruction
import mysql.connector
import pandas as pd
import os
from math import *
from django.shortcuts import render, redirect
from django.forms import ModelForm, Textarea
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from collections import defaultdict
import sys 
sys.path.append('/Users/alexissoltysiak/Documents/GitHub/ERPsim-helper/django_server/erpsim_helper/pythonAlgorithms')

#sys.path.append('/Users/alexissoltysiak/Documents/GitHub/ERPsim-helper/django_server/erpsim_helper/')

import variables as var

from ..models import Tips

 




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
    #LocalisationsInventaire = var.LocalisationsInventaire

    #Donner une approximation des parametres
    dfSales = createDf(mydb,"sales")
    """dfInventory = createDf(mydb,"inventory")"""
    #os.system('clear')

    company = str(joueur+set)

    rounds, jours = test(var.mydb,company)
    #print("Round : ",rounds,"   Jour : ",jours)
    #print("")

    findParameters = trouverParametres(dfSales,company,Materials,Localisations)

    return findParameters

def materialDef():
  return ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]

def getReapro():
  material = materialDef()

  reapro = {}

  reaproMilk = 900
  reaproCream = 300
  reaproYoghurt = 700
  reaproCheese = 350
  reaproButter = 400
  reaproIceCream = 300
  
  reapro[material[0]]=reaproMilk
  reapro[material[1]]=reaproCream
  reapro[material[2]]=reaproYoghurt
  reapro[material[3]]=reaproCheese
  reapro[material[4]]=reaproButter
  reapro[material[5]]=reaproIceCream

  return reapro

def insertDB (ListeReaproJoueur, db):

  for i in ListeReaproJoueur.items():

    if (i[1][0]!=1):

      ListOfPreviousTips = Tips.objects.filter(element=i[0])
      ListOfPreviousTips.update(is_active=False)

      sentenceToAdd = str( "Augmentez le prix du produit " + str(i[0].upper()) + " à " + str(i[1][1]))
      I = Tips(company_code="A4",date_time=datetime.now(),element = i[0],sentence=sentenceToAdd ,is_active=True )
      I.save()
      
  return

def getMatriceStock(prediction, stock_actuel, equipe, jour_du_cycle):
  materials = materialDef()
  reapro=getReapro()

  if jour_du_cycle != 1:
    return 0

  matrice_stock={}

  for element in materials:
    somme_coef = prediction[element][0] + prediction[element][1] + prediction[element][2]
    #Dispatch du produit "element" dans les 3 entrepots
    dispatch_element=[]
    for i in range (0,3):
      dispatch_theorique = prediction[element][i] / somme_coef
      if (dispatch_theorique * reapro[element] > stock_actuel[element]):
        dispatch_element.append(floor(dispatch_theorique * reapro[element] - stock_actuel[element]))
      else:
        dispatch_element.append(0)

    #Unites non reparties dans les entrepots secondaires
    reste = reapro[element] - dispatch_element[0] - dispatch_element[1] - dispatch_element[2]

    matrice_stock[element]=[dispatch_element[0]+floor(reste/3)]

  return(matrice_stock)







ventes_veille={"Milk":[5,5,4],"Cream":[5,5,4],"Yoghurt":[5,5,4],"Cheese":[5,5,4],"Butter":[5,5,4],"Ice Cream":[5,5,4]}
prix = {"Milk":45,"Cream":56,"Yoghurt":40,"Cheese":40,"Butter":40,"Ice Cream":40}
stock_actuel = {"Milk":[300,50,65],"Cream":[300,50,65],"Yoghurt":[300,50,65],"Cheese":[300,50,65],"Butter":[300,50,65],"Ice Cream":[300,50,65]}
frequence=5
jour_cycle=2
equipe="L9"

def getMatricePrix(ventes_veille, prix_actuels, frequence_reapro, jour_du_cycle, stock_actuel, equipe):
  materials = materialDef()
  jours_cycle_restants = frequence_reapro + 1 - jour_du_cycle

  dictionnaire_prix = {}

  for element in materials:
    if (ventes_veille[element][0] >= stock_actuel[element][0]/jours_cycle_restants or ventes_veille[element][1] >= stock_actuel[element][1]/jours_cycle_restants or ventes_veille[element][2] >= stock_actuel[element][2]/jours_cycle_restants):
      dictionnaire_prix[element]=[1.1, 1.1*prix_actuels[element]]
    elif (ventes_veille[element][0] < 0.8*stock_actuel[element][0]/jours_cycle_restants and ventes_veille[element][1] < 0.8*stock_actuel[element][1]/jours_cycle_restants and ventes_veille[element][2] < 0.8*stock_actuel[element][2]/jours_cycle_restants):
      dictionnaire_prix[element]=[0.9, 0.9*prix_actuels[element]]
    else:
      dictionnaire_prix[element]=[1, prix_actuels[element]]

  insertDB(dictionnaire_prix, var.mydb)

  return dictionnaire_prix

print(getMatricePrix(ventes_veille, prix, frequence, jour_cycle, stock_actuel, equipe))

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


  insertDB(ListeReaproJoueur, var.mydb)

  return ListeReaproJoueur



def getTheTipsBack():

  ListOfTips = Tips.objects.filter(is_active=True)

  return(ListOfTips)
