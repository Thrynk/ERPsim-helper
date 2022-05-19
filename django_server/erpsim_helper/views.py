from django.shortcuts import render
from django.forms import Form, CharField, PasswordInput
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Game, Player, Sales, Inventory
from .tasks import get_game_latest_data
from .plots.plotly_plot import plotly_plot_sales, plotly_plot_stocks

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

    products = ["Cream", "Ice Cream", "Butter", "Milk", "Cheese", "Yoghurt"]

    # pass sales to plotly_plot
    sales_evolution_plot, sales_distribution_plot = plotly_plot_sales(sales, products)
    stock_evolution_plot = plotly_plot_stocks(inventory, products)

    context = {'sales_evolution_plot': sales_evolution_plot, 'sales_distribution_plot': sales_distribution_plot, 'stock_evolution_plot': stock_evolution_plot}

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