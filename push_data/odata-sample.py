import pyodata
from pyodata.v2.model import PolicyFatal, PolicyWarning, PolicyIgnore, ParserError, Config
import requests

import mysql.connector

# import logging
# logging.basicConfig()
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.DEBUG)

SERVICE_URL = 'https://gordon.hec.ca:8001/odata/345' #'http://e02lp1.ucc.in.tum.de:8002/odata/904'

session = requests.Session()
session.auth = ('M_1', '05ABCabc')

TABLES_SQL = ['inventory', 'pricing_conditions', 'sales']
TABLES_ODATA = ['Inventory', 'Pricing_Conditions', 'Sales']

CHAMPS_SQL = ['inventory_opening_balance, row_number, plant, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, storage_location, material_number, material_description, material_type, material_code, material_label, unit',
        'price, sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, material_number, material_description, distribution_channel, dc_name, currency',
        'sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, sales_order_number, line_item, storage_location, region, area, city, country, postal_code, customer_number, distribution_channel, material_number, material_description, material_type, material_code, material_label, quantity, quantity_delivered, unit, net_price, net_value, cost, currency, contribution_margin, contribution_margin_pct']
CHAMPS_ODATA = [champ.upper() for champ in CHAMPS_SQL]

table_souhaitée = 1     # 0, 1 ou 2

"""# namespaces = {
#     'edmx': 'customEdmxUrl.com',
#     'edm': 'customEdmUrl.com'
# }

# custom_config = Config(
#     xml_namespaces=namespaces,
#     default_error_policy=PolicyFatal(),
#     custom_error_policies={
#          ParserError.ANNOTATION: PolicyWarning(),
#          ParserError.ASSOCIATION: PolicyIgnore()
#     })
# service = pyodata.Client(SERVICE_URL, session, config=custom_config)"""


service = pyodata.Client(SERVICE_URL, session)
entity_set_names = [es.name for es in service.schema.entity_sets]

for ent in entity_set_names :
    for id, table in enumerate(TABLES_ODATA) :
        if ent == table :
            print(f"Entity : {ent}")
            print(CHAMPS_ODATA[id])
            print(id)
            try :
                response = service.entity_sets.__getattr__(ent).get_entities().select(CHAMPS_ODATA[id]).execute()
            except : 
                print("Un champ n'est pas dans les données")

            """
            for rep in response :
                print(rep.ROW_NUMBER)"""


# sales = service.entity_sets.Pricing_Contibutions.get_entities().select(CHAMPS_ODATA[table_souhaitée].upper()).execute()

#print(sales)

#print(len(sales))

#for sale in sales :
#    print(f"Row number : {sale.ROW_NUMBER}, Price : {sale.PRICE}, Sales organization : {sale.SALES_ORGANIZATION}")
    #print(sale.AREA, sale.REGION)

# Pour mettre en base de données : 
# sql = "INSERT INTO Log (userName, passWord, typeCompte, Nom) VALUES (?, ?, ?, ?)"
# value = (username.get(), str(hasher2.digest()), Compte.get(), name.get())

try : 
    cnx = mysql.connector.connect(user='odata', password='xGf#57PsB?td',
                                host='127.0.0.1',
                                database='erpsim_games')

    cnx.close()

except : 
    print("Error during the connexion")