# IMPORTS 
import pyodata
from pyodata.v2.model import PolicyFatal, PolicyWarning, PolicyIgnore, ParserError, Config
import requests
import mysql.connector
import os
import time

# VARIABLES STATIQUES 
JEU_EN_COURS = True 

#'http://e02lp1.ucc.in.tum.de:8002/odata/904'
SERVICE_URL = os.environ.get("ODATA_URL")

"""TABLES_SQL = [
            'inventory', 
            'pricing_conditions', 
            'sales',
            'company_valuation',
            'current_inventory'
            'current_inventory_kpi'
            ]
TABLES_ODATA = [
            'Inventory', 
            'Pricing_Conditions', 
            'Sales',
            'Company_Valuation',
            'Current_Inventory',
            'Current_Inventory_KPI'
            ]

CHAMPS_SQL = [
        'inventory_opening_balance, row_number, plant, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, storage_location, material_number, material_description, material_type, material_code, material_label, unit',
        'price, sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, material_number, material_description, distribution_channel, dc_name, currency',
        'sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, sales_order_number, line_item, storage_location, region, area, city, country, postal_code, customer_number, distribution_channel, material_number, material_description, material_type, material_code, material_label, quantity, quantity_delivered, unit, net_price, net_value, cost, currency, contribution_margin, contribution_margin_pct',
        'row_number, company_code, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, bank_cash_account, accounts_receivable, bank_loan, accounts_payable, profit, debt_loading, credit_rating, company_risk_rate_pct, company_valuation, currency',
        'row_number, plant, material_number, material_description, storage_location, stock, restricted, unit',
        'row_number, plant, storage_location, material_number, material_description, material_type, material_code, material_label, current_inventory, quantity_sold, nb_steps_available, sim_elapsed_steps, unit'
        ]

CHAMPS_ODATA = [champ.upper() for champ in CHAMPS_SQL]"""


# DEFINITION DES FONCTIONS 
def add_data_into_mysql(table, response):
    list_data = []
    for rep in response : 
        record = tuple([rep.__getattr__(chp.upper()) for chp in CHAMPS_SQL[table]])
        list_data.append(record)
    
    insert_statement = "INSERT INTO " + table + "(" + ",".join(CHAMPS_SQL[table]) + ") VALUES(" + ",".join(["%s"] * len(CHAMPS_SQL[table])) + ")"
    
    return insert_statement, list_data

"""
Fonction extract_data_once qui prend en argument ......... 
Elle charge en une fois toutes les données du flux odata pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_once():
    print("*****Chargement d'une partie terminée... *****")
    """print(TABLES_SQL)
    print(CHAMPS_SQL)
    print(ENTITY_SET_NAMES)"""
    # print(TABLES_SQL)
    
    d1 = time.time()
    for table in TABLES_SQL :
        print(f"Chargement de la table {table}")
        table_odata_name = [table_odata for table_odata in ENTITY_SET_NAMES if table_odata.lower() == table.lower()][0]
        
        response = service.entity_sets.__getattr__(table_odata_name).get_entities().execute()
        query, list_data = add_data_into_mysql(table, response) 

        try : 
            mycursor = cnx.cursor()
            mycursor.executemany(query, list_data)
            cnx.commit()
        except : 
            print("Un champ n'est pas dans les données")

    print(f"\n--- Temps d'éxecution : {time.time()-d1}")
    print("\n\n*****Chargement réussi !*****")
    return True


"""
Fonction extract_data_loop qui prend en argument ......... 
Elle charge les (nouvelles) données du flux odata toutes les x secondes pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_loop():
    print("Partie en cours...")
    
    d1 = time.time()
    for table in TABLES_SQL :
        print(f"Chargement de la table {table}")
        table_odata_name = [table_odata for table_odata in ENTITY_SET_NAMES if table_odata.lower() == table.lower()][0]
        
        response = service.entity_sets.__getattr__(table_odata_name).get_entities().execute()
        query, list_data = add_data_into_mysql(table, response) 

        #try : 
        mycursor = cnx.cursor()
        mycursor.executemany(query, list_data)
        cnx.commit()
        #except : 
        #    print("Un champ n'est pas dans les données")
        

    print(f"\n--- Temps d'éxecution : {time.time()-d1}")
    print("\n\n*****Chargement réussi !*****")
    return True


# MAIN 
if __name__ == "__main__" :
    connexion = True

    d1 = time.time()
    # CONNEXIONS 
    try :
        session = requests.Session()
        session.auth = (os.environ.get("ODATA_USER"), os.environ.get("ODATA_PASSWORD"))
        service = pyodata.Client(SERVICE_URL, session)
    except : 
        connexion = False
        print("Error during the connexion to the odata flux")

    try : 
        cnx = mysql.connector.connect(user=os.environ.get("DATABASE_USER"), password=os.environ.get("DATABASE_PASSWORD"),
                                    host=os.environ.get("DATABASE_HOST"),
                                    database=os.environ.get("DATABASE"))
    except : 
        connexion = False
        print("Error during the connexion to mySQL")

    print(f"\n--- Durée des deux connexions : {time.time() - d1}")
    # Si la connexion est faite on lance le programme
    if connexion : 
        # Demande si les données qui vont être chargées viennent d'une partie en cours ou d'une partie terminée. 
        JEU_EN_COURS = int(input("Vous chargez les données d'une partie (1)En cours ou d'une partie (2)Terminée ? ")) == 1

        d1 = time.time()
        ENTITY_SET_NAMES = [es.name for es in service.schema.entity_sets]

        mycursor = cnx.cursor()
        mycursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='" + os.environ.get("DATABASE") + "'")

        TABLES_SQL = [elem[0] for elem in mycursor.fetchall()]
        CHAMPS_SQL = dict()

        print(f"\n--- Temps pour aller chercher les différentes tables dans le information_schema.tables {time.time()-d1}")
        for table in TABLES_SQL : 
            mycursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='" + os.environ.get("DATABASE") +"' AND table_name = '" + table + "' AND column_key<>'PRI'")
            CHAMPS_SQL[table] = [elem[0] for elem in mycursor.fetchall()]

        # Lancement des fonctions en conséquence.
        if JEU_EN_COURS :
            extract_data_loop()
        else :
            extract_data_once()