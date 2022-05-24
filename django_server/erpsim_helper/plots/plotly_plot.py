import pandas as pd
from plotly.offline import plot
from .drawFigures import drawSalesEvolution, drawSalesDistribution, drawStocks, drawEmptySales, drawEmptyStocks
from ..models import Inventory


def plotly_plot_sales(sales, products):
    """
    This function display plotly plots related to sales.
    :param:
    """
    columns = ['row_number', 'sales_organization', 'sim_calendar_date', 'storage_location', 'material_label',
               'quantity']
    df_sales = pd.DataFrame(list(sales.values(*columns)), columns=columns)

    if df_sales.empty:
        sales_evolution_graph, sales_distribution_graph = drawEmptySales()
    else:
        # Conversion des types
        columns_type = {'sales_organization': 'string', 'storage_location': 'string', 'material_label': 'string'}
        df_sales = df_sales.astype(columns_type)

        # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
        df_sales["sim_calendar_date"] = pd.to_datetime(df_sales["sim_calendar_date"], format="%d/%m/%Y %H:%M")

        # Tri du tableau par ROW_NUMBER
        df_sales.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

        sales_evolution_graph, dataframe_company_products = drawSalesEvolution(df_sales, products)
        sales_distribution_graph, dataframe_company_allstorages = drawSalesDistribution(df_sales, products)

    # Turn graph object into local plotly graph
    plotly_plot_obj1 = plot({'data': sales_evolution_graph}, output_type='div')
    plotly_plot_obj2 = plot({'data': sales_distribution_graph}, output_type='div')

    return plotly_plot_obj1, plotly_plot_obj2


def plotly_plot_stocks(inventory, products):
    """
    This function display plotly plots related to stocks
    """
    columns = ['inventory_opening_balance', 'row_number', 'plant', 'sim_calendar_date', 'storage_location',
               'material_label']
    df_inventory = pd.DataFrame(list(inventory.values(*columns)), columns=columns)

    if df_inventory.empty:
        stock_evolution_graph = drawEmptyStocks()
    else:
        # Conversion des types
        columns_type = {'plant': 'string', 'storage_location': 'string', 'material_label': 'string'}
        df_inventory = df_inventory.astype(columns_type)

        # Conversion de la colonne SIM_CALENDAR_DATE au format datetime
        df_inventory["sim_calendar_date"] = pd.to_datetime(df_inventory["sim_calendar_date"], format="%d/%m/%Y %H:%M")

        # Tri du tableau par ROW_NUMBER
        df_inventory.sort_values(by=["row_number"], axis=0, inplace=True, ignore_index=True)

        stock_evolution_graph, general, nord, sud, ouest = drawStocks(df_inventory, products)

    # Turn graph object into local plotly graph
    plotly_plot_obj1 = plot({'data': stock_evolution_graph}, output_type='div')

    return plotly_plot_obj1
