from huey.contrib.djhuey import task, enqueue

import pyodata
from pyodata.v2.service import GetEntitySetFilter as esf

import requests
import mysql.connector
import os
import time
import logging
import datetime

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

odata_service = None
logger = logging.getLogger("huey")
try: 
    sql_conn = mysql.connector.connect(
        pool_name = "odata_pool",
        pool_size = 20,
        user=os.environ.get("DATABASE_USER"), 
        password=os.environ.get("DATABASE_PASSWORD"),
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE")
    )
except : 
    print("Error during the connexion to mySQL")

@task()
def get_game_latest_data(game_id, odata_flow, game_set, team, is_running, odata_user, odata_password):
    """
        Build group of tasks in order to get the data. 

        This function is used to create one task for each table in the BDD. Moreover, 
        it creates one task one table for each 60 seconds. (One day in the simulation is 1 minute). 
        So, we have, a group of tasks, with a table to reach and a datetime to execute it. 

        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 
        :param odata_flow: It is the address of the flow which contains the data. 
        :type odata_flow: str 
        :param game_set: Set used for the game 
        :type game_set: int
        :param team: All the teams they are playing the game (A, B, C, ...)
        :type team: list['str']
        :param is_running: True if the game is running, False otherwise.
        :type is_running: Boolean
        :param odata_user: Credentials, Log In
        :type odata_user: str
        :param odata_password: Credentials
        :type odata_password: str
    """
    logger.info('-- game_id : {} flow : {} set : {} team : {} is_running : {} --'.format(game_id, odata_flow, game_set, team, is_running))

    global odata_service

    # CONNEXIONS 
    #try :
    session = requests.Session()
    # session.auth = (os.environ.get("ODATA_USER"), os.environ.get("ODATA_PASSWORD"))
    session.auth = (odata_user, odata_password)
    odata_service = pyodata.Client(odata_flow, session)
    #or("Error during the connexion to the odata flux")

    TABLES_SQL = TABLE_SOCIETE.keys()  

    # launch store_table tasks
    d1 = time.time()
    tasks_group = []
    for table in TABLES_SQL:
        # schedule tasks to fetch data every minute (every round day in ERPSim)
        for i in range(100): # 8 rounds of 10 virtual days (+ 20 if round duration = 1'30)
            eta = datetime.datetime.now() + datetime.timedelta(seconds=60 * i)
            tasks_group.append(store_table.schedule((table, game_id, game_set, team), eta=eta))   
    #result_group = [enqueue(t) for t in tasks_group]
    #result_group = [result.get(True) for result in tasks_group]
    #task_group = store_table.map([(table, game_id, game_set, team) for table in TABLES_SQL])
    #task_group.get(blocking=True)
    logger.info(f"Execution time of all tasks : {time.time() - d1}")    

@task()
def store_table(table, game_id, game_set, team):
    """
        Store the data into sql database. 

        This function is used to reach data on the odata flow. It enables to have the 
        data at one time, for one table, of all teams on one game. 

        :param table: Odata Table to reach
        :type table: str
        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 
        :param game_set: Set used for the game 
        :type game_set: int
        :param team: All the teams they are playing the game (A, B, C, ...)
        :type team: list['str']
    """
    entity_set_names = [es.name for es in odata_service.schema.entity_sets]

    sql_conn = mysql.connector.connect(pool_name = "odata_pool")

    d1 = time.time()
    logger.info(f"Chargement de la table {table}")
    table_odata_name = [table_odata for table_odata in entity_set_names if table_odata.lower() == table.lower()][0]

    # Si on joue sur les sets 2 à 9 les équipes sont A2, B2, ..., A9, B9
    if game_set != 1 :
        list = [lettre + str(game_set) for lettre in team]
    # Si on joue sur le set 1, les équipes sont AA, BB, CC, ....
    else : 
        list = [lettre + lettre for lettre in team]
        
    filter = " or ".join([TABLE_SOCIETE[table].upper() + " eq '" + society + "'" for society in list])

    try : 
        max_date = get_max_sim_date(sql_conn, table, game_id)[0]

        response = odata_service.entity_sets.__getattr__(table_odata_name).get_entities()
        response = response.filter(filter and response.SIM_CALENDAR_DATE>max_date).execute()
        query, list_data = generate_statement_data(sql_conn, table, response, game_id) 
    except :
        # delete from table where id_game = id_game 
        sql = f"DELETE FROM {table} WHERE id_game={str(game_id)};"

        try : 
            mycursor = sql_conn.cursor()
            mycursor.execute(sql)
            sql_conn.commit()
        except: 
            logger.error(f"Erreur lors de la suppression des données dans la table {table}")

        response = odata_service.entity_sets.__getattr__(table_odata_name).get_entities()
        response = response.filter(filter).execute()
        query, list_data = generate_statement_data(sql_conn, table, response, game_id) 
    # Push les données 
    add_data_into_mysql(sql_conn, query, list_data)
    sql_conn.close()

    logger.info(f"\n--- Execution time for table {table} : {time.time()-d1}")
    return True


def get_max_sim_date(sql_conn, table, id_game):
    """
        Get max simulation date.

        It returns the last tuple (`round`, `step`) in the database.

        :param sql_conn: SQL connector created in :py:function:store_table
        :type sql_conn: 
        :param table: Odata Table to reach
        :type table: str
        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 

        :return: (`round`, `step`)
        :rtype: tuple()
    """
    mycursor = sql_conn.cursor()
    mycursor.execute(f"SELECT max(sim_calendar_date) FROM {table} WHERE id_game={str(id_game)};")
    return mycursor.fetchone()


def generate_statement_data(sql_conn, table, response, id_game):
    """
        Generate statement ton insert data into sql database

        It creates `list_data` which each tuple contains one line of data of the odata flow. 
        It creates the insert statement for the next insertion. 

        :param sql_conn: SQL connector created in :py:function:store_table
        :type sql_conn: 
        :param table: Odata Table to reach
        :type table: str
        :param response: Data
        :type response: dict
        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 

        :return: (SQL statement, data) to push in the database
        :rtype: tuple()
    """
    mycursor = sql_conn.cursor()
    mycursor.execute(f"\
        SELECT \
            column_name \
        FROM information_schema.columns \
        WHERE table_schema='{os.environ.get('DATABASE')}' \
        AND table_name = '{table}' \
        AND column_key<>'PRI' AND column_name<>'id_game'"
    )

    fields = [elem[0] for elem in mycursor.fetchall()]

    list_data = []
    for rep in response : 
        record = (id_game,) + tuple([rep.__getattr__(chp.upper()) for chp in fields])
        list_data.append(record)
    
    insert_statement = f"INSERT INTO {table} (id_game, {','.join(fields)}) VALUES({','.join(['%s'] * (len(fields)+1))})"
    return insert_statement, list_data


"""
Fonction add_data_into_mysql pour push les données dans la base de données
"""
def add_data_into_mysql(sql_conn, query, data):
    """
        Push data into sql database

        :param sql_conn: SQL connector created in :py:function:store_table
        :type sql_conn: 
        :param query: Insert Statement
        :type query: str
        :param data: Data
        :type data: Dict
    """
    try : 
        mycursor = sql_conn.cursor()
        mycursor.executemany(query, data)
        sql_conn.commit()
    except : 
        logger.error("Un champ n'est pas dans les données")