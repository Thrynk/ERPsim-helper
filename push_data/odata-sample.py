import pyodata
from pyodata.v2.model import PolicyFatal, PolicyWarning, PolicyIgnore, ParserError, Config
import requests

# import logging
# logging.basicConfig()
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.DEBUG)

SERVICE_URL = 'http://e02lp1.ucc.in.tum.de:8002/odata/904'

session = requests.Session()
session.auth = ('Z_2', '21ISENisen')

# namespaces = {
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


# service = pyodata.Client(SERVICE_URL, session, config=custom_config)
service = pyodata.Client(SERVICE_URL, session)

sales = service.entity_sets.Sales.get_entities().select('SIM_DATE').execute()

#print(sales)

print(len(sales))

for sale in sales:
    print(sale.SIM_DATE)
    #print(sale.AREA, sale.REGION)