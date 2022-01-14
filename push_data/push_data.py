# IMPORTS 
import pyodata
from pyodata.v2.model import PolicyFatal, PolicyWarning, PolicyIgnore, ParserError, Config
from pyodata.v2.service import GetEntitySetFilter as esf
import requests
import mysql.connector
import os
import time

# VARIABLES STATIQUES 
JEU_EN_COURS = True 

#'http://e02lp1.ucc.in.tum.de:8002/odata/904'
SERVICE_URL = os.environ.get("ODATA_URL")

# MAPPING TABLE - SOCIETE
TABLE_SOCIETE = {   "company_valuation"         : "company_code", 
                    "current_inventory"         : "plant",
                    "current_inventory_kpi"     : "plant", 
                    "current_suppliers_prices"  : "purchasing_organization", 
                    "financial_postings"        : "company_code", 
                    "goods_movements"           : "plant", 
                    "independent_requirements"  : "plant", 
                    "inventory"                 : "plant", 
                    "market"                    : "company_code", 
                    "nps_surveys"               : "plant", 
                    "pricing_conditions"        : "sales_organization", 
                    "purchase_orders"           : "company_code",
                    "sales"                     : "sales_organization", 
                    "stock_transfers"           : "plant", 
                    "suppliers_prices"          : "purchasing_organization"}

# DEFINITION DES FONCTIONS 
"""
Fonction generate_statement_data qui prend en argument une table et les données envoyées par le flux odata
Elle crée list_data, une liste de tuples, chaque tuple contient une ligne de données du flux odata. 
Elle crée aussi insert_statement qui correspond à la requete SQL pour insérer les données en base 
Renvoie insert_statement et list_data
"""
def generate_statement_data(table, response, id_game):
    list_data = []
    for rep in response : 
        record = (id_game,) + tuple([rep.__getattr__(chp.upper()) for chp in CHAMPS_SQL[table]])
        list_data.append(record)
    
    insert_statement = f"INSERT INTO {table} (id_game, {','.join(CHAMPS_SQL[table])}) VALUES({','.join(['%s'] * (len(CHAMPS_SQL[table])+1))})"
    return insert_statement, list_data

"""
Fonction get_max_sim_round qui prend en argument une table 
Elle renvoie le dernier couple (round, step) inséré en base. 
"""
def get_max_sim_date(table, id_game):
    mycursor = cnx.cursor()
    mycursor.execute(f"SELECT max(sim_calendar_date) FROM {table} WHERE id_game={str(id_game)};")
    return mycursor.fetchone()


"""
Fonction add_data_into_mysql pour push les données dans la base de données
"""
def add_data_into_mysql(query, data):
    try : 
        mycursor = cnx.cursor()
        mycursor.executemany(query, data)
        cnx.commit()
    except : 
        print("Un champ n'est pas dans les données")

"""
Fonction extract_data_once qui prend en argument ......... 
Elle charge en une fois toutes les données du flux odata pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_once(id_game, team, set):
    print("*****Chargement d'une partie terminée... *****")
    
    d1 = time.time()
    for table in TABLES_SQL :
        print(f"Chargement de la table {table}")
        table_odata_name = [table_odata for table_odata in ENTITY_SET_NAMES if table_odata.lower() == table.lower()][0]

        list = [lettre + str(set) for lettre in team]
        filter = " or ".join([TABLE_SOCIETE[table].upper() + " eq '" + society + "'" for society in list])
        
        try : 
            response = service.entity_sets.__getattr__(table_odata_name).get_entities()
            response = response.filter(filter).execute()
            query, list_data = generate_statement_data(table, response, id_game) 
        except:
            print(f"Erreur lors du chargement de la table {table}")

        # Push les données 
        add_data_into_mysql(query, list_data)

    print(f"\n--- Temps d'éxecution : {time.time()-d1}")
    print("\n\n*****Chargement réussi !*****")
    return True


"""
Fonction extract_data_loop qui prend en argument ......... 
Elle charge les (nouvelles) données du flux odata toutes les x secondes pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_loop(id_game, team, set):
    print("Partie en cours...")
    
    d1 = time.time()
    for table in TABLES_SQL :
        print(f"Chargement de la table {table}")
        table_odata_name = [table_odata for table_odata in ENTITY_SET_NAMES if table_odata.lower() == table.lower()][0]

        list = [lettre + str(set) for lettre in team]
        filter = " or ".join([TABLE_SOCIETE[table].upper() + " eq '" + society + "'" for society in list])

        try : 
            max_date = get_max_sim_date(table, id_game)[0]

            response = service.entity_sets.__getattr__(table_odata_name).get_entities()
            response = response.filter(filter and response.SIM_CALENDAR_DATE>max_date).execute()
            query, list_data = generate_statement_data(table, response, id_game) 
        except :
            # delete from table where id_game = id_game 
            sql = f"DELETE FROM {table} WHERE id_game={str(id_game)};"

            try : 
                mycursor = cnx.cursor()
                mycursor.execute(sql)
                cnx.commit()
            except: 
                print(f"Erreur lors de la suppression des données dans la table {table}")

            response = service.entity_sets.__getattr__(table_odata_name).get_entities()
            response = response.filter(filter).execute()
            query, list_data = generate_statement_data(table, response, id_game) 

        # Push les données 
        add_data_into_mysql(query, list_data)

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

        # TABLES_SQL = [elem[0] for elem in mycursor.fetchall()]
        TABLES_SQL = TABLE_SOCIETE.keys()
        CHAMPS_SQL = dict()

        print(f"\n--- Temps pour aller chercher les différentes tables dans le information_schema.tables {time.time()-d1}")
        for table in  TABLES_SQL: 
            mycursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='" + os.environ.get("DATABASE") +"' AND table_name = '" + table + "' AND column_key<>'PRI' AND column_name<>'id_game'")
            CHAMPS_SQL[table] = [elem[0] for elem in mycursor.fetchall()]

        id_game=4
        team="JKLM"
        set=9
        # Lancement des fonctions en conséquence.
        if JEU_EN_COURS :
            extract_data_loop(id_game, team, set)
        else :
            extract_data_once(id_game, team, set)