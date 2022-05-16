
def table_pricing_conditions(response):
    list_data = []

    for rep in response :
        list_data.append((float(rep.PRICE), rep.SALES_ORGANIZATION, rep.ROW_NUMBER, rep.SIM_ROUND, rep.SIM_STEP, rep.SIM_CALENDAR_DATE, rep.SIM_PERIOD, rep.SIM_ELAPSED_STEPS, rep.MATERIAL_NUMBER, rep.MATERIAL_DESCRIPTION, rep.DISTRIBUTION_CHANNEL, rep.DC_NAME, rep.CURRENCY))
            
    add_pricing_conditions = "\
                        INSERT INTO pricing_conditions_test \
                        (price, sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, material_number, material_description, distribution_channel, dc_name, currency) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    return add_pricing_conditions, list_data

def table_inventory(response): 
    list_data = []

    for rep in response : 
        list_data.append((rep.INVENTORY_OPENING_BALANCE, rep.ROW_NUMBER, rep.PLANT, rep.SIM_ROUND, rep.SIM_STEP, rep.SIM_CALENDAR_DATE, rep.SIM_PERIOD, rep.SIM_ELAPSED_STEPS, rep.STORAGE_LOCATION, rep.MATERIAL_NUMBER, rep.MATERIAL_DESCRIPTION, rep.MATERIAL_TYPE, rep.MATERIAL_CODE, rep.MATERIAL_LABEL, rep.UNIT))

    add_inventory = "\
        INSERT INTO inventory \
        (inventory_opening_balance, row_number, plant, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, storage_location, material_number, material_description, material_type, material_code, material_label, unit) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    return add_inventory, list_data

def table_sales(response): 
    list_data = []

    for rep in response : 
        list_data.append((rep.SALES_ORGANIZATION, rep.ROW_NUMBER, rep.SIM_ROUND, rep.SIM_STEP, rep.SIM_CALENDAR_DATE, rep.SIM_PERIOD, rep.SIM_ELAPSED_STEPS, rep.SALES_ORDER_NUMBER, rep.LINE_ITEM, rep.STORAGE_LOCATION, rep.REGION, rep.AREA, rep.CITY, rep.COUNTRY, rep.POSTAL_CODE, rep.CUSTOMER_NUMBER, rep.DISTRIBUTION_CHANNEL, rep.MATERIAL_NUMBER, rep.MATERIAL_DESCRIPTION, rep.MATERIAL_TYPE, rep.MATERIAL_CODE, rep.MATERIAL_LABEL, rep.QUANTITY, rep.QUANTITY_DELIVERED, rep.UNIT, rep.NET_PRICE, rep.NET_VALUE, rep.COST, rep.CURRENCY, rep.CONTRIBUTION_MARGIN, rep.CONTRIBUTION_MARGIN_PCT))

    add_inventory = "\
        INSERT INTO sales \
        (sales_organization, row_number, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, sales_order_number, line_item, storage_location, region, area, city, country, postal_code, customer_number, distribution_channel, material_number, material_description, material_type, material_code, material_label, quantity, quantity_delivered, unit, net_price, net_value, cost, currency, contribution_margin, contribution_margin_pct) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    return add_inventory, list_data

def table_company_valuation(response): 
    list_data = []

    for rep in response : 
        list_data.append((rep.ROW_NUMBER, rep.COMPANY_CODE, rep.SIM_ROUND, rep.SIM_STEP, rep.SIM_CALENDAR_DATE, rep.SIM_PERIOD, rep.SIM_ELAPSED_STEPS, rep.BANK_CASH_ACCOUNT, rep.ACCOUNTS_RECEIVABLE, rep.BANK_LOAN, rep.ACCOUNTS_PAYABLE, rep.PROFIT, rep.DEBT_LOADING, rep.CREDIT_RATING, rep.COMPANY_RISK_RATE_PCT, rep.COMPANY_VALUATION, rep.CURRENCY))

    add_inventory = "\
        INSERT INTO company_valuation \
        (row_number, company_code, sim_round, sim_step, sim_calendar_date, sim_period, sim_elapsed_steps, bank_cash_account, accounts_receivable, bank_loan, accounts_payable, profit, debt_loading, credit_rating, company_risk_rate_pct, company_valuation, currency) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    return add_inventory, list_data

def table_current_inventory(response): 
    list_data = []

    for rep in response : 
        list_data.append((rep.ROW_NUMBER, rep.PLANT, rep.MATERIAL_NUMBER, rep.MATERIAL_DESCRIPTION, rep.STORAGE_LOCATION, rep.STOCK, rep.RESTRICTED, rep.UNIT))

    add_inventory = "\
        INSERT INTO current_inventory \
        (row_number, plant, material_number, material_description, storage_location, stock, restricted, unit) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
    return add_inventory, list_data

def table_current_inventory_kpi(response): 
    list_data = []

    for rep in response : 
        list_data.append((rep.ROW_NUMBER, rep.PLANT, rep.STORAGE_LOCATION, rep.MATERIAL_NUMBER, rep.MATERIAL_DESCRIPTION, rep.MATERIAL_TYPE, rep.MATERIAL_CODE, rep.MATERIAL_LABEL, rep.CURRENT_INVENTORY, rep.QUANTITY_SOLD, rep.NB_STEPS_AVAILABLE, rep.SIM_ELAPSED_STEPS, rep.UNIT))

    add_inventory = "\
        INSERT INTO current_inventory_kpi \
        (row_number, plant, storage_location, material_number, material_description, material_type, material_code, material_label, current_inventory, quantity_sold, nb_steps_available, sim_elapsed_steps, unit) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    return add_inventory, list_data