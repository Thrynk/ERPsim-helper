import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def addNoSalesData(dataframe, products, dateRange=None, storage=False):
    """
    Add data in the dataframe on day where there is no sales. Use to plot curve of sales
    :param dataframe: Sales dataframe
    :param dateRange: dateRange object
    :param products: string or list of products to display
    :param storage: boolean if the function is called to display storage distribution
    :return: New dataframe with no sales line added, group by day and product
    """
    if isinstance(products, str): products = [products]

    if storage:
        storages = storages = ["03N", "03S", "03W"]
        for storage in storages:
            for product in products:
                if not dataframe.index.isin([(storage, product)]).any():
                    dataframe.loc[(storage, product), "quantity"] = 0
        dataframe = dataframe.groupby(["storage_location", "material_label"]).sum()
        dataframe = dataframe.sort_index(level="material_label")

    else:
        for date in dateRange:
            for product in products:
                if not dataframe.index.isin([(date, product)]).any():
                    dataframe.loc[(date, product), "quantity"] = 0
        dataframe = dataframe.groupby(["sim_calendar_date", "material_label"]).sum()
        dataframe = dataframe.sort_index(level="sim_calendar_date")

    dataframe = dataframe.astype({'quantity': 'int64'})

    return dataframe


def drawSalesDistribution(dataframe, company, products, startDate=None, endDate=None):
    """
    Description : Gives dataframe of sales group by storage location and display the graph
    :param dataframe: Sales dataframe
    :param company: Company name
    :param products: String or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of sales group by storage location and products and display the plot
    """
    dataframe_company = dataframe[dataframe["sales_organization"] == company]
    dataframe_company = dataframe_company.reset_index(drop=True)
    storages = ["03N", "03S", "03W"]
    storages_names = ["nord", "sud", "ouest"]

    if startDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] >= startDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        startDate = dataframe_company.loc[0, "sim_calendar_date"]

    if endDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] <= endDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        endDate = dataframe_company.loc[len(dataframe_company) - 1, "sim_calendar_date"]

    if isinstance(products, str): products = [products]

    plt.switch_backend('AGG')
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 14))
    plt.suptitle("Répartition des ventes dans les régions", size=20)

    dataframe_company_allstorages = dataframe_company[
        ["sim_calendar_date", "storage_location", "material_label", "quantity"]]
    dataframe_company_allstorages = dataframe_company_allstorages[
        dataframe_company_allstorages["material_label"].isin(products)]
    dataframe_company_allstorages = dataframe_company_allstorages.groupby(["storage_location", "material_label"]).sum()
    dataframe_company_allstorages = addNoSalesData(dataframe_company_allstorages, products, storage=True)

    for storage, storage_name, i in zip(storages, storages_names, range(1, len(storages) + 1)):
        dataframe_company_storage = dataframe_company_allstorages.loc[(storage), :]

        plt.subplot(3, 1, i)
        plt.title(f"Entrepôt {storage_name}")
        plt.bar(dataframe_company_storage.index.values, dataframe_company_storage.loc[:, "quantity"])
        plt.xlabel("Produits")
        plt.ylabel("Quantité vendue")

    plt.subplots_adjust(hspace=0.3)
    plt.tight_layout(rect=[0, 0.03, 1, 0.98])

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return dataframe_company_allstorages, graph


def drawSalesEvolution(dataframe, company, products, startDate=None, endDate=None):
    """
    Display one graph of the evolution of the sales
    :param dataframe: Sales dataframe
    :param company: Company name
    :param products: string or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of sales group by day and products and display the plot
    """
    dataframe_company = dataframe[dataframe["sales_organization"] == company]
    dataframe_company = dataframe_company.reset_index(drop=True)

    if startDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] >= startDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        startDate = dataframe_company.loc[0, "sim_calendar_date"]

    if endDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] <= endDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        endDate = dataframe_company.loc[len(dataframe_company) - 1, "sim_calendar_date"]

    dateRange = pd.date_range(start=startDate, end=endDate)
    dateRange.freq = None
    xlabel = dateRange.tolist()
    xlabel = [timestamp.date() for timestamp in xlabel]

    if isinstance(products, str): products = [products]

    plt.switch_backend('AGG')
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))
    plt.title("Évolution des ventes")
    plt.xlabel("Date")
    plt.ylabel("Nombre de ventes")
    plt.xticks(dateRange, xlabel, rotation=45)

    dataframe_company_products = dataframe_company[dataframe_company["material_label"].isin(products)]
    dataframe_company_products = dataframe_company_products[
        ["sim_calendar_date", "material_label", "quantity"]].groupby(["sim_calendar_date", "material_label"]).sum()
    dataframe_company_products = addNoSalesData(dataframe_company_products, products, dateRange)

    for product in products:
        dataframe_product = dataframe_company_products.xs(key=product, level=1)
        plt.plot(dateRange, dataframe_product["quantity"], label=product)

    plt.legend(bbox_to_anchor=(1.0, 1.0))

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return dataframe_company_products, graph


def drawStocks(dataframe, company, products, startDate=None, endDate=None):
    """
    Description : Gives 4 dataframes of stock evolution by storage location and display the graph
    :param dataframe: Stock dataframe
    :param company: Company name
    :param products: String or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of stock evolution group by storage location and display the plot
    """
    dataframe_company = dataframe[dataframe["plant"] == company]
    dataframe_company = dataframe_company.reset_index(drop=True)

    if startDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] >= startDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        startDate = dataframe_company.loc[0, "sim_calendar_date"]

    if endDate:
        dataframe_company = dataframe_company[dataframe_company["sim_calendar_date"] <= endDate]
        dataframe_company = dataframe_company.reset_index(drop=True)
    else:
        endDate = dataframe_company.loc[len(dataframe_company) - 1, "sim_calendar_date"]

    dateRange = pd.date_range(start=startDate, end=endDate)
    dateRange.freq = None
    xlabel = dateRange.tolist()
    xlabel = [timestamp.date() for timestamp in xlabel]

    if isinstance(products, str):
        products = [products]

    plt.style.use('ggplot')
    plt.figure(figsize=(14, 10))
    plt.suptitle("Évolution des stocks", size=20)

    # Entrepot général
    dataframe_company_general = dataframe_company[dataframe_company["storage_location"] == "03"]
    dataframe_company_general = dataframe_company_general[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    dataframe_company_general.drop_duplicates(inplace=True)
    # Entrepot Nord
    dataframe_company_north = dataframe_company[dataframe_company["storage_location"] == "03N"]
    dataframe_company_north = dataframe_company_north[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    dataframe_company_north.drop_duplicates(inplace=True)
    # Entrepot Sud
    dataframe_company_south = dataframe_company[dataframe_company["storage_location"] == "03S"]
    dataframe_company_south = dataframe_company_south[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    dataframe_company_south.drop_duplicates(inplace=True)
    # Entrepot Ouest
    dataframe_company_west = dataframe_company[dataframe_company["storage_location"] == "03W"]
    dataframe_company_west = dataframe_company_west[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    dataframe_company_west.drop_duplicates(inplace=True)

    for product in products:
        dataframe_company_general_product = dataframe_company_general[
            dataframe_company_general["material_label"] == product]
        dataframe_company_north_product = dataframe_company_north[dataframe_company_north["material_label"] == product]
        dataframe_company_south_product = dataframe_company_south[dataframe_company_south["material_label"] == product]
        dataframe_company_west_product = dataframe_company_west[dataframe_company_west["material_label"] == product]

        plt.subplot(2, 2, 1)
        plt.title("Entrepot général")
        plt.plot(dateRange, dataframe_company_general_product["inventory_opening_balance"], label=product)
        plt.xticks(dateRange, xlabel, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Quantité en stock")

        plt.subplot(2, 2, 2)
        plt.title("Entrepot Nord")
        plt.plot(dateRange, dataframe_company_north_product["inventory_opening_balance"], label=product)
        plt.xticks(dateRange, xlabel, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Quantité en stock")

        plt.subplot(2, 2, 3)
        plt.title("Entrepot Sud")
        plt.plot(dateRange, dataframe_company_south_product["inventory_opening_balance"], label=product)
        plt.xticks(dateRange, xlabel, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Quantité en stock")

        plt.subplot(2, 2, 4)
        plt.title("Entrepot Ouest")
        plt.plot(dateRange, dataframe_company_west_product["inventory_opening_balance"], label=product)
        plt.xticks(dateRange, xlabel, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Quantité en stock")

    plt.subplots_adjust(wspace=0.2, hspace=0.45)
    plt.legend(bbox_to_anchor=(1.3, 1.4))

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return dataframe_company_general, dataframe_company_north, dataframe_company_south, dataframe_company_west, graph


if __name__ == "__main__":
    df_sales = pd.read_csv("./catalog/data/11-01-2022/Sales.csv", encoding="latin", delimiter=";", decimal=",")

    # Suppression des colonnes inutiles
    df_sales.drop(["SIM_DATE", "SALES_ORDER_NUMBER", "LINE_ITEM", "REGION", "CITY", "COUNTRY", "POSTAL_CODE",
                   "DISTRIBUTION_CHANNEL", "MATERIAL_NUMBER", "MATERIAL_DESCRIPTION", "MATERIAL_TYPE", "MATERIAL_SIZE",
                   "QUANTITY_DELIVERED", "UNIT", "CURRENCY"], axis=1, inplace=True)

    # Conversion des types
    columns_type = {'ID': 'string', 'SALES_ORGANIZATION': 'string', 'STORAGE_LOCATION': 'string',
                    'MATERIAL_CODE': 'string', 'MATERIAL_LABEL': 'string', 'NET_PRICE': 'float64',
                    'NET_VALUE': 'float64',
                    'COST': 'float64', 'CONTRIBUTION_MARGIN': 'float64', 'CONTRIBUTION_MARGIN_PCT': 'float64',
                    'AREA': 'category'}

    df_sales = df_sales.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_sales["SIM_CALENDAR_DATE"] = pd.to_datetime(df_sales["SIM_CALENDAR_DATE"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_sales.sort_values(by=["ROW_NUMBER"], axis=0, inplace=True, ignore_index=True)

    print(df_sales)
