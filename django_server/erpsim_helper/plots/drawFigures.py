import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


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
        storages = ["03N", "03S", "03W"]
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


def drawSalesDistribution(dataframe_company, products, startDate=None, endDate=None):
    """
    Display one graph of the distribution of the sales in the storage
    :param dataframe: Sales dataframe
    :param company: Company name
    :param products: String or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of sales group by storage location and products and display the plot
    """
    dataframe_company = dataframe_company.reset_index(drop=True)
    storages = ["03N", "03S", "03W"]
    storages_names = ["Nord", "Sud", "Ouest"]

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

    dataframe_company_allstorages = dataframe_company[
        ["sim_calendar_date", "storage_location", "material_label", "quantity"]]
    dataframe_company_allstorages = dataframe_company_allstorages[
        dataframe_company_allstorages["material_label"].isin(products)]
    dataframe_company_allstorages = dataframe_company_allstorages.groupby(["storage_location", "material_label"]).sum()
    dataframe_company_allstorages = addNoSalesData(dataframe_company_allstorages, products, storage=True)

    fig = make_subplots(rows=3, cols=1, x_title="Produits", y_title="Quantité vendue",
                        subplot_titles=[storage_name for storage_name in storages_names],
                        vertical_spacing=0.1)

    for storage, storage_name, i in zip(storages, storages_names, range(1, len(storages) + 1)):
        dataframe_company_storage = dataframe_company_allstorages.loc[(storage), :]
        fig.add_trace(go.Bar(x=dataframe_company_storage.index.values, y=dataframe_company_storage.loc[:, "quantity"],
                             hovertemplate="(%{x}, %{y})<extra></extra>"), row=i, col=1)

    fig.update_layout(
        title="Répartition des ventes dans les régions",
        title_xanchor="center",
        title_x=0.5,
        showlegend=False,
        height=700,
        width=600,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )

    return fig, dataframe_company_allstorages


def drawSalesEvolution(dataframe_company, products, startDate=None, endDate=None):
    """
    Display one graph of the evolution of the sales
    :param dataframe: Sales dataframe
    :param company: Company name
    :param products: String or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of sales group by day and products and display the plot
    """
    
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

    dataframe_company_products = dataframe_company[dataframe_company["material_label"].isin(products)]
    dataframe_company_products = dataframe_company_products[
        ["sim_calendar_date", "material_label", "quantity"]].groupby(["sim_calendar_date", "material_label"]).sum()
    dataframe_company_products = addNoSalesData(dataframe_company_products, products, dateRange)

    # Create graph object Figure object with data
    fig = go.Figure()

    for product in products:
        dataframe_product = dataframe_company_products.xs(key=product, level=1)
        fig.add_trace(go.Scatter(x=dateRange, y=dataframe_product["quantity"], name=product))

    fig.update_layout(
        title="Évolution des ventes",
        title_xanchor="center",
        title_x=0.45,
        xaxis_title="Date",
        xaxis_tickformat="%e %b %Y",
        xaxis_tickangle=-30,
        width=800,
        yaxis_title="Nombre de ventes",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )

    return fig, dataframe_company_products


def drawStocks(dataframe_company, products, startDate=None, endDate=None):
    """
    Gives 4 dataframes of stock evolution by storage location and display the graph
    :param dataframe: Stock dataframe
    :param company: Company name
    :param products: String or list of products to display
    :param startDate: First day to display
    :param endDate: Last day to display
    :return: New dataframe of stock evolution group by storage location and display the plot
    """
    warehouse_names = ["général", "Nord", "Sud", "Ouest"]
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

    # Entrepot général
    dataframe_company_general = dataframe_company[dataframe_company["storage_location"] == "03"]
    dataframe_company_general = dataframe_company_general[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    # Entrepot Nord
    dataframe_company_north = dataframe_company[dataframe_company["storage_location"] == "03N"]
    dataframe_company_north = dataframe_company_north[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    # Entrepot Sud
    dataframe_company_south = dataframe_company[dataframe_company["storage_location"] == "03S"]
    dataframe_company_south = dataframe_company_south[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]
    # Entrepot Ouest
    dataframe_company_west = dataframe_company[dataframe_company["storage_location"] == "03W"]
    dataframe_company_west = dataframe_company_west[
        ["sim_calendar_date", "material_label", "inventory_opening_balance"]]

    fig = make_subplots(rows=2, cols=2, x_title="Date", y_title="Quantité en stock",
                        subplot_titles=[f"Entrepôt {warehouse_name}" for warehouse_name in warehouse_names],
                        vertical_spacing=0.2)

    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]
    legendgroup_list = ["group1", "group2", "group3", "group4", "group5", "group6"]

    for product, color, legendgroup in zip(products, colors, legendgroup_list):
        dataframe_company_general_product = dataframe_company_general[
            dataframe_company_general["material_label"] == product]
        dataframe_company_north_product = dataframe_company_north[dataframe_company_north["material_label"] == product]
        dataframe_company_south_product = dataframe_company_south[dataframe_company_south["material_label"] == product]
        dataframe_company_west_product = dataframe_company_west[dataframe_company_west["material_label"] == product]

        fig.add_trace(go.Scatter(x=dateRange, y=dataframe_company_general_product["inventory_opening_balance"],
                                 name=product, line_color=color, legendgroup=legendgroup), row=1, col=1)
        fig.add_trace(go.Scatter(x=dateRange, y=dataframe_company_north_product["inventory_opening_balance"],
                                 name=product, line_color=color, legendgroup=legendgroup, showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=dateRange, y=dataframe_company_south_product["inventory_opening_balance"],
                                 name=product, line_color=color, legendgroup=legendgroup, showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=dateRange, y=dataframe_company_west_product["inventory_opening_balance"],
                                 name=product, line_color=color, legendgroup=legendgroup, showlegend=False), row=2, col=2)

    fig.update_layout(
        title="Évolution des stocks",
        title_xanchor="center",
        title_x=0.47,
        height=700,
        width=850,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )

    for ax in fig['layout']:
        if ax[:5] == 'xaxis':
            fig['layout'][ax]['tickformat'] = "%e %b %Y"
            fig['layout'][ax]['tickangle'] = -30

    for ax in fig['layout']:
        if ax[:11] == "annotations":
            for index, annotation in enumerate(fig['layout'][ax]):
                if fig['layout'][ax][index]['text'] == "Date":
                    fig['layout'][ax][index]['y'] = -0.07
                if fig['layout'][ax][index]['text'] == "Quantité en stock":
                    fig['layout'][ax][index]['x'] = -0.04

    return fig, dataframe_company_general, dataframe_company_north, dataframe_company_south, dataframe_company_west


def drawEmptySales():
    """
    Generate empty figures for sales evolution and distribution with text "Pas de données à afficher" displayed.
    """
    empty_sales_evolution = go.Figure().add_trace(go.Scatter(x=[0], y=[0], marker=dict(color="crimson")))
    empty_sales_evolution.add_annotation(x=0, y=0, text="Pas de données à afficher", font=dict(family="sans serif", size=25,
                                                                              color="crimson"), showarrow=False, yshift=10)
    empty_sales_evolution.update_layout(
        title="Évolution des ventes",
        title_xanchor="center",
        title_x=0.5,
        xaxis_visible=False,
        yaxis_visible=False,
        width=800,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )
    empty_sales_distribution = go.Figure().add_trace(go.Scatter(x=[0], y=[0], marker=dict(color="crimson")))
    empty_sales_distribution.add_annotation(x=0, y=0, text="Pas de données à afficher", font=dict(family="sans serif", size=25,
                                                                              color="crimson"), showarrow=False, yshift=10)
    empty_sales_distribution.update_layout(
        title="Répartition des ventes dans les régions",
        title_xanchor="center",
        title_x=0.5,
        xaxis_visible=False,
        yaxis_visible=False,
        height=700,
        width=650,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )

    return empty_sales_evolution, empty_sales_distribution


def drawEmptyStocks():
    """
    Generate empty figures for stocks distribution graph with text "Pas de données à afficher" displayed.
    """
    empty_stock_evolution = go.Figure().add_trace(go.Scatter(x=[0], y=[0], marker=dict(color="crimson")))
    empty_stock_evolution.add_annotation(x=0, y=0, text="Pas de données à afficher",
                                         font=dict(family="sans serif", size=25,
                                                   color="crimson"), showarrow=False, yshift=10)
    empty_stock_evolution.update_layout(
        title="Évolution des stocks",
        title_xanchor="center",
        title_x=0.47,
        height=700,
        width=800,
        xaxis_visible=False,
        yaxis_visible=False,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )

    return empty_stock_evolution
