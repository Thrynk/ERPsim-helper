import pandas as pd
import numpy as np

##########################################
# INITIALISATION
##########################################

joueur = input(" Lettre du Joueur ? : ").upper()

Materials = ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]
Localisations = ["North","South","West"]
LocalisationsInventaire = ["03","03N","03S","03W"]

ListeSalesJoueur =[[] for i in range (3)]
ListeCA=[]
tableauVentesQuotidiennes = []
tableauVentesRound = []
tableauVentesTotal = []

##########################################
# Fonctions INFORMATIVES
##########################################

#Fonction pour renvoyer les sales avec ROUND et STEP ( jour ) comme argument
def SalesTable(joueur,Round=None,Step=None):

    #Pré affichage 
    print("\nJoueur ", joueur," / Round ",Round," / Step ", Step)
    print("")
    print("Nord / Sud / West")

    #On garde les valeurs du joueur
    csvSalesJoueur = csvSales[csvSales["SALES_ORGANIZATION"].astype(str).str.startswith(str(joueur))]

    ListeSalesJoueur =[[] for i in range (3)]

    #On garde le round et le jour qu'on veut 
    if (Round!= None):
        csvSalesJoueur = csvSalesJoueur[csvSalesJoueur["SIM_ROUND"]==Round]
    if (Step!=None):
        csvSalesJoueur = csvSalesJoueur[csvSalesJoueur["SIM_STEP"]==Step]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvSalesJoueurMaterial = csvSalesJoueur[csvSalesJoueur["MATERIAL_LABEL"]==material]
        tmp=[]
        for localisation in Localisations:
            if len(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"])==0:
                tmp.append(0)
            else:
                tmp.append(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"].sum())
       
        print(material,tmp)
        ListeSalesJoueur.append(tmp)
    
    return ListeSalesJoueur


#Fonction POURCENTAGES pour renvoyer les sales avec ROUND et STEP ( jour ) comme argument
def SalesTablePercent(joueur,Round=None,Step=None,Precision=0):

    #Pré affichage 
    print("\nJoueur ", joueur," / Round ",Round," / Step ", Step)
    print("PERCENTAGE")
    print("")
    print("Nord / Sud / West")

    #On garde les valeurs du joueur
    csvSalesJoueur = csvSales[csvSales["SALES_ORGANIZATION"].astype(str).str.startswith(str(joueur))]

    ListeSalesJoueur =[[] for i in range (3)]

    #On garde le round et le jour qu'on veut 
    if (Round!= None):
        csvSalesJoueur = csvSalesJoueur[csvSalesJoueur["SIM_ROUND"]==Round]
    if (Step!=None):
        csvSalesJoueur = csvSalesJoueur[csvSalesJoueur["SIM_STEP"]==Step]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvSalesJoueurMaterial = csvSalesJoueur[csvSalesJoueur["MATERIAL_LABEL"]==material]
        tmp=[]
        somme=0
        for localisation in Localisations:
            if len(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"])==0:
                tmp.append(0)
            else:
                tmp.append(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"].sum())
                somme+=csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"].sum()
       
        for i in range (len(tmp)):
            if(somme!=0):
                if Precision == 0:
                    tmp[i]=int(100*tmp[i]/somme)
                else:
                    tmp[i]=round(100*tmp[i]/somme,Precision)
            else :
                tmp[i]="None"

        
        for j in range (len(tmp)):
            if(tmp[i]!="None"):
                tmp[j] = str(tmp[j]) + "%"
            

        print(material,tmp)
        ListeSalesJoueur.append(tmp)
    
    return ListeSalesJoueur

def trouverParametres(csvSales,precision=250):

    #Affichage
    print("Les parametres tendent vers : ")
    print(" ")

    ListeSalesJoueur =[[] for i in range (3)]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvSalesJoueurMaterial = csvSales[csvSales["MATERIAL_LABEL"]==material]
        tmp=[]
        for localisation in Localisations:
            if len(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"])==0:
                tmp.append(0)
            else:
                tmp.append(round(csvSalesJoueurMaterial[csvSalesJoueurMaterial["AREA"]==localisation]["QUANTITY"].sum()/precision,0))
       
        print(material,tmp)
        ListeSalesJoueur.append(tmp)
    
    return ListeSalesJoueur

def chiffredAffaire(joueur,Round=None,Step=None):

    #Pré affichage 
    print("\nJoueur ", joueur," / Round ",Round," / Step ", Step)
    print("")

    ListeCA = []
    #On garde les valeurs du joueur
    csvCAJoueur = csvSales[csvSales["SALES_ORGANIZATION"].astype(str).str.startswith(str(joueur))]

    #On garde le round et le jour qu'on veut 
    if (Round!= None):
        csvCAJoueur = csvCAJoueur[csvCAJoueur["SIM_ROUND"]==Round]
    if (Step!=None):
        csvCAJoueur = csvCAJoueur[csvCAJoueur["SIM_STEP"]==Step]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvCAJoueurMaterial = csvCAJoueur[csvCAJoueur["MATERIAL_LABEL"]==material]


        tmp = csvCAJoueurMaterial['COST'].tolist()

        tmp = [float(i.replace(',','.')) for i in tmp]
        CA= int(sum (tmp))

       
        print(material,CA, "€")
        ListeCA.append(CA)
    
    return ListeCA


def inventory(joueur,Round,Step):

    #Pré affichage 
    print("\nJoueur ", joueur," / Round ",Round," / Step ", Step)
    print("")
    print("General / Nord / Sud / West")

    #On garde les valeurs du joueur
    csvInventoryJoueur = csvInventory[csvInventory["PLANT"].astype(str).str.startswith(str(joueur))]

    #On garde le round et le jour qu'on veut 
    csvInventoryJoueur  = csvInventoryJoueur [csvInventoryJoueur ["SIM_ROUND"]==Round]
    csvInventoryJoueur  = csvInventoryJoueur [csvInventoryJoueur ["SIM_STEP"]==Step]

    Listeinventaire=[]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvInventoryJoueurMaterial = csvInventoryJoueur[csvInventoryJoueur["MATERIAL_LABEL"]==material]
        tmp=[]
        for localisation in LocalisationsInventaire:
            if len(csvInventoryJoueurMaterial[csvInventoryJoueurMaterial["STORAGE_LOCATION"]==localisation]["INVENTORY_OPENING_BALANCE"])==0:
                tmp.append(0)
            else:
                tmp.append(csvInventoryJoueurMaterial[csvInventoryJoueurMaterial["STORAGE_LOCATION"]==localisation]["INVENTORY_OPENING_BALANCE"].sum())
       
        print(material,tmp)
        Listeinventaire.append(tmp)


    return Listeinventaire


def princingConditions(joueur,Round,Step):

    #Pré affichage 
    print("\nJoueur ", joueur," / Round ",Round," / Step ", Step)
    print("")
    print("Princing")

    csvPricingJoueur = csvPricing[csvPricing["SALES_ORGANIZATION"].astype(str).str.startswith(str(joueur))]

    listePricing=[]

    #On garde le round et le jour qu'on veut 
    csvPricingJoueur  = csvPricingJoueur [csvPricingJoueur ["SIM_ROUND"]==Round]
    csvPricingJoueur = csvPricingJoueur [csvPricingJoueur ["SIM_STEP"]==Step]

    #Iteration Matériaux et Localisation
    for material in Materials:
        csvPricingJoueurMaterial = csvPricingJoueur[csvPricingJoueur["MATERIAL_DESCRIPTION"]==material]
        tmp = int(csvPricingJoueurMaterial["PRICE"])
        listePricing.append(tmp)
        print(material,tmp,"€")
 

    return listePricing




##########################################
# Fonctions ALGO
##########################################



##########################################
# Affichage données 
##########################################

#Récupere le CSV
csvSales = pd.read_csv("OData ISA set 5 Sales 05-10-2021.csv", encoding="latin",delimiter = ";")
csvInventory = pd.read_csv("OData ISA set 5 Inventory 05-10-2021.csv", encoding="latin",delimiter = ";")
csvPricing = pd.read_csv("OData ISA set 5 Pricing Conditions 05-10-2021.csv", encoding="latin",delimiter = ";")



#Si on veut les sales totales
SalesTable(joueur)

#Si on veut un round particulier
SalesTable(joueur,Round=1)

#Si on veut un jour d'un round particulier
SalesTable(joueur,Round=1,Step=8)

#POURCENTAGE 
#Si on veut un jour d'un round particulier en pourcentage
SalesTablePercent(joueur,Round=1,Step=4)

#Si on veut un pourcentage des les sales totales avec une meilleure précision
SalesTablePercent(joueur,Precision=2)

print("trouver parametres")
#Donner une approximation des parametres
trouverParametres(csvSales)

#Donner le chiffre d'affaire par produit
chiffredAffaire(joueur,Round=3)

#Exemple d'inventaire se vidant + stock 
inventory("A",3,5) 
inventory("A",3,6) 
SalesTable("A",Round=3,Step=6)
inventory("A",3,7)

#CA round / jour => CA jour

princingConditions(joueur,3,4)



trouverParametres(csvSales)























