import mysql.connector
import pandas as pd
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="odata",
    password="xGf#57PsB?td",
    port="3306"
)

#Creation des parametres en INPUT
joueur = "L"
set = "9"

Materials = ["Milk","Cream","Yoghurt","Cheese","Butter","Ice Cream"]
Localisations = ["North","South","West"]
LocalisationsInventaire = ["03","03N","03S","03W"]

reaproMilk = 900
reaproCream = 300
reaproYoghurt = 700
reaproCheese = 350
reaproButter = 400
reaproIceCream = 300

company = str(joueur+set)

quantiteReapro = [reaproMilk, reaproCream, reaproYoghurt, reaproCheese, reaproButter, reaproIceCream]
frequenceReapro = 5
ventes     = [170,60,150,65,40,50]
