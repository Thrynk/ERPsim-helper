import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from .utils import getSalesData, getInventoryData
from .drawFigures import drawSalesEvolution, drawSalesDistribution, drawStocks


def plotly_plot_sales(mysql_connection, company, products):
    """
    This function display plotly plots
    """
    df_sales = getSalesData(mysql_connection)

    # Conversion des types
    columns_type = {'sales_organization': 'string', 'storage_location': 'string', 'material_label': 'string'}
    df_sales = df_sales.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_sales["sim_calendar_date"] = pd.to_datetime(df_sales["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_sales.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    fig1, dataframe_company_products = drawSalesEvolution(df_sales, company, products)
    fig2, dataframe_company_allstorages = drawSalesDistribution(df_sales, company, products)
    # Turn graph object into local plotly graph
    plotly_plot_obj1 = plot({'data': fig1}, output_type='div')
    plotly_plot_obj2 = plot({'data': fig2}, output_type='div')

    return plotly_plot_obj1, plotly_plot_obj2


def plotly_plot_stocks(mysql_connection, company, products):
    """
    This function display plotly plots
    """
    df_inventory = getInventoryData(mysql_connection)

    # Conversion des types
    columns_type = {'plant': 'string', 'storage_location': 'string', 'material_label': 'string'}
    df_inventory = df_inventory.astype(columns_type)

    # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
    df_inventory["sim_calendar_date"] = pd.to_datetime(df_inventory["sim_calendar_date"], format="%d/%m/%Y %H:%M")

    # Tri du tableau par ROW_NUMBER
    df_inventory.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

    fig1, general, nord, sud, ouest = drawStocks(df_inventory, company, products)

    # Turn graph object into local plotly graph
    plotly_plot_obj1 = plot({'data': fig1}, output_type='div')

    return plotly_plot_obj1
