from django.shortcuts import render
from django.forms import Form, CharField, PasswordInput
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Max

from django.contrib.auth.decorators import login_required

from .models import Game, Player, Sales, Inventory, PricingConditions, CompanyValuation
from .tasks import get_game_latest_data
from .plots.plotly_plot import plotly_plot_sales, plotly_plot_stocks

from .strategies.alexis_charles import prediction, getMatriceStock, getMatricePrix

# Create your views here.
class ContactForm(Form):
    """
        The ContactForm object is usefull for login. 

        To be connected with the odata flow, we have to fill : 
        * The number of the game (Game ID)
        * The login 
        * The password
    """
    gameNumber = CharField(max_length=200)
    login = CharField(max_length=200)
    password = CharField(widget=PasswordInput, max_length=200)

@login_required
def index(request):     # TO DO
    """
        Redirect if user is not logged in, else display dashboard page. 

        :param request:
        :type request: django.http.HttpRequest

        :return: Http response
        :rtype: Http response
    """
    player_associated_with_user = Player.objects.get(user=request.user.id)

    game = Game.objects.get(pk=player_associated_with_user.game_id)

    if game.game_set == 1:
        company_name = request.user.username[0] + request.user.username[0]
    else:
        company_name = request.user.username[0] + str(game.game_set)

    sales = Sales.objects.filter(id_game=game.id, sales_organization=company_name)

    inventory = Inventory.objects.filter(id_game=game.id, plant=company_name)

    products = ["Milk", "Cream", "Yoghurt", "Cheese", "Butter", "Ice Cream"]

    # pass sales to plotly_plot
    sales_evolution_plot, sales_distribution_plot = plotly_plot_sales(sales, products)
    stock_evolution_plot = plotly_plot_stocks(inventory, products)

    # Generate tips

    # Generate expected format for sales data to send to prediciton function
    max_sim_elapsed_steps = sales.aggregate(sim_elapsed_steps=Max('sim_elapsed_steps'))
    sales_previous_day = [sale for sale in sales if sale.sim_elapsed_steps == max_sim_elapsed_steps["sim_elapsed_steps"]]

    sales_per_storage_per_material = {
        "Milk": [0,0,0], "Cream":[0,0,0], "Yoghurt":[0,0,0], "Cheese":[0,0,0], "Butter":[0,0,0], "Ice Cream":[0,0,0]
    }
    for sale in sales_previous_day:
        if sale.storage_location == "03N":
            sales_per_storage_per_material[sale.material_label][0] = sale.quantity
        elif sale.storage_location == "03S":
            sales_per_storage_per_material[sale.material_label][1] = sale.quantity
        elif sale.storage_location == "03W":
            sales_per_storage_per_material[sale.material_label][2] = sale.quantity
    print("Sales :")
    print(sales_per_storage_per_material)

    # Generate price data in expected format
    prices = PricingConditions.objects.filter(id_game=game.id, sales_organization=company_name)
    last_price_update = prices.aggregate(sim_elapsed_steps=Max('sim_elapsed_steps'))

    prices = [price for price in prices if price.sim_elapsed_steps == last_price_update["sim_elapsed_steps"]]
    prices_dict = {}
    for price in prices:
        prices_dict[price.material_description] = price.price

    # print("Prices :")
    # print(prices_dict)

    # Generate inventory data in expected format
    last_stock_update_step = inventory.aggregate(sim_elapsed_steps=Max('sim_elapsed_steps'))

    stocks = [stock for stock in inventory if stock.sim_elapsed_steps == last_stock_update_step["sim_elapsed_steps"]]
    stocks_per_storage_per_material = {
        "Milk": [0,0,0,0], "Cream":[0,0,0,0], "Yoghurt":[0,0,0,0], "Cheese":[0,0,0,0], "Butter":[0,0,0,0], "Ice Cream":[0,0,0,0]
    }
    for stock in stocks:
        if stock.storage_location == "03N":
            stocks_per_storage_per_material[stock.material_label][0] = stock.inventory_opening_balance
        elif stock.storage_location == "03S":
            stocks_per_storage_per_material[stock.material_label][1] = stock.inventory_opening_balance
        elif stock.storage_location == "03W":
            stocks_per_storage_per_material[stock.material_label][2] = stock.inventory_opening_balance
        elif stock.storage_location == "03":
            stocks_per_storage_per_material[stock.material_label][3] = stock.inventory_opening_balance

    print("stocks :")
    print(stocks_per_storage_per_material)

    day = CompanyValuation.objects.filter(id_game=game.id, company_code=company_name).aggregate(sim_elapsed_steps=Max('sim_elapsed_steps'))["sim_elapsed_steps"]
    print(f"day: {day}")

    procurement_frequency = 5
    #print({'tips':getTheTipsBack(),'predictions':getMatriceStock(prediction("test"),stocks_per_storage_per_material, company_name, day % procurement_frequency),'material':materialDef,'modifPrix':getMatricePrix(sales_per_storage_per_material, prices_dict, procurement_frequency, day % procurement_frequency, stocks_per_storage_per_material, company_name)})

    if day is None:
        stock_matrix = None
        prices_matrix_name_converted = None
        day = 1
    else:
        parameters = prediction(sales, company_name, products)

        stock_matrix = getMatriceStock(parameters, products, stocks_per_storage_per_material, company_name, day % procurement_frequency)
        print(stock_matrix)

        prices_matrix = getMatricePrix(
            sales_per_storage_per_material,
            prices_dict,
            day % procurement_frequency,
            stocks_per_storage_per_material,
            products,
            procurement_frequency
        )
        print(prices_matrix)

        # init a dict to match material_description (eg. Milk) with material_number (eg.OO-T01)
        name_conversion_for_material = {material["material_description"]: material["material_number"] for material in list(inventory.order_by('material_number', 'material_description').values('material_number', 'material_description').distinct())}
        
        # generate dict with key: OO-T01, because this is the format in ERPsim to change prices
        prices_matrix_name_converted = {}
        for material_description, material_number in name_conversion_for_material.items():
            prices_matrix_name_converted[material_number] = prices_matrix[material_description]

    context = {
        'sales_evolution_plot': sales_evolution_plot,
        'sales_distribution_plot': sales_distribution_plot,
        'stock_evolution_plot': stock_evolution_plot,
        'username': request.user.username,
        'round': int(day / 8) + 1 if int(day / 8) == 0 else int(day / 8),
        'step': day % 10,
        'sim_elapsed_steps': day,
        'material': products,
        'predictions': stock_matrix,
        'modifPrix': prices_matrix_name_converted
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)

    #return HttpResponse(f"Hello, Player : {request.user.username} from company {company_name}. \n Your associated game is {player_associated_with_user.game_id}.")


def game(request, game_id):     # TO DO
    """
        Get the current game. 

        :param request:
        :type request:
        :param game_id: ID of the game that we want to reach the data 
        :type game_id: int 
    """
    game = Game.objects.get(pk=game_id)
    return HttpResponse(f"Game page : {game.id} \n Flux odata : {game.odata_flow}.")