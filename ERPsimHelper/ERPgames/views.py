from django.shortcuts import render
from .plotly_plot import plotly_plot_sales, plotly_plot_stocks
from .utils import dbConnexion


def index(request):
    mysql_connection = dbConnexion()

    # Plotly visualizations
    sales_evolution_plot, sales_distribution_plot = plotly_plot_sales(mysql_connection, "C9", ["Cream", "Ice Cream", "Butter", "Milk", "Cheese", "Yoghurt"])
    stock_evolution_plot = plotly_plot_stocks(mysql_connection, "C9", ["Cream", "Ice Cream", "Butter", "Milk", "Cheese", "Yoghurt"])

    # Return context to home page view
    context = {'sales_evolution_plot': sales_evolution_plot, 'sales_distribution_plot': sales_distribution_plot,
               'stock_evolution_plot': stock_evolution_plot}

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)
