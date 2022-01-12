import mysql.connector
import pandas as pd
import os

#######################################
# Parameters 
#######################################

#Connection a la BDD SQL 
mydb = mysql.connector.connect(
  host="localhost",
  user="odata",
  password="xGf#57PsB?td",
  port="3306"
)

#Creation des parametres en INPUT 
joueur = "C"
set = "9"

Materials = ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]
Localisations = ["North","South","West"]
LocalisationsInventaire = ["03","03N","03S","03W"]


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
  Cursor.execute("USE erpsim_games_temp")
  cmd = str("SELECT * FROM "+table)
  Cursor.execute(cmd)

  CursorName = mydb.cursor()
  CursorName.execute("USE erpsim_games_temp")
  cmd = str("SELECT column_name FROM information_schema.columns WHERE table_schema='erpsim_games_temp' AND table_name='"+table+"'")
  CursorName.execute(cmd)

  df = cursorToCsv(Cursor,CursorName)
  return df
  

#######################################
# Find the matrice 
#######################################

def trouverParametres(df,sales_organization,precision=10):

    #Affichage
    print("Les parametres tendent vers : ")
    print(" ")

    ListeSalesJoueur =[[] for i in range (3)]

    df=df[df["sales_organization"]==sales_organization]

    #Iteration Matériaux et Localisation
    for material in Materials:
        dfSalesJoueurMaterial = df[df['material_label']==material]
        tmp=[]
        for localisation in Localisations:
            if len(dfSalesJoueurMaterial[dfSalesJoueurMaterial["area"]==localisation]["quantity"])==0:
                tmp.append(0)
            else:
                tmp.append(round(dfSalesJoueurMaterial[dfSalesJoueurMaterial["area"]==localisation]["quantity"].sum()/precision,0))
       
        print(material,tmp)
        ListeSalesJoueur.append(tmp)
    
    return ListeSalesJoueur

for i in range(100):
  print(i)
  #Donner une approximation des parametres
  dfSales = createDf(mydb,"sales")
  dfInventory = createDf(mydb,"inventory")
  os.system('clear')
  trouverParametres(dfSales,str(joueur+set))
