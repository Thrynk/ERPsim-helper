import pandas as pd
from math import floor 

def get_sales_repartition(df,materials,localisations,precision=80):
    """
        Get the repartition of sales of each product in each region based on historical data

        :param df: Previous sales
        :type df: pd.DataFrame
        :param materials: list of products
        :type materials: list
        :param localisations: name of the 3 locations (north, south and west here)
        :type localisations: list

        :return: sales_repartition_dict
        :rtype: dict
    """

    # If the dataframe is empty, it means we don't have sales yet, then we send a default dict
    if df.empty:
        return {material: [0,0,0] for material in materials}

    # We calculate the sales proportion for each product in each region
    df_sales_repartition = df.groupby(["material_label", "area"])["quantity"].sum() / df.groupby(["material_label"])["quantity"].sum()

    # We convert the dataframe into a dict for future usage
    sales_repartition_dict = {material: [0,0,0] for material in materials}

    for index, row in df_sales_repartition.reset_index().iterrows():
        sales_repartition_dict[row.material_label][localisations.index(row.area)] = round(row.quantity, 2)

    return sales_repartition_dict

def getReapro(materials):
    """
        Give the quantity that are delivered to the main warehouse for each product(thoses are constant in our scenario)

        It returns a dict

        :param materials: names of the sold items
        :type sales: list

        :return: reapro
        :rtype: dict
    """

    reapro = {}

    reaproMilk = 900
    reaproCream = 300
    reaproYoghurt = 700
    reaproCheese = 350
    reaproButter = 400
    reaproIceCream = 300

    reapro[materials[0]]=reaproMilk
    reapro[materials[1]]=reaproCream
    reapro[materials[2]]=reaproYoghurt
    reapro[materials[3]]=reaproCheese
    reapro[materials[4]]=reaproButter
    reapro[materials[5]]=reaproIceCream

    return reapro


def getCostPrices(materials):
    """
        Give the unit buy prices by the company for each product

        It returns a dict

        :param materials: names of the sold items
        :type materials: list

        :return: Minimum price for each product
        :rtype: dict
    """

    cost_prices = {}

    costMilk = 22.95
    costCream = 72.07
    costYoghurt = 25.85
    costCheese = 82.68
    costButter = 59.88
    costIceCream = 43.15

    cost_prices[materials[0]] = costMilk
    cost_prices[materials[1]] = costCream
    cost_prices[materials[2]] = costYoghurt
    cost_prices[materials[3]] = costCheese
    cost_prices[materials[4]] = costButter
    cost_prices[materials[5]] = costIceCream

    return cost_prices

def getMatriceStock(prediction, materials, stock_actuel):
    """
        Give the stock dispatch advices that must be applied as push in ERP Sim

        It returns a dict

        :param prediction: predicted market preferences
        :type prediction: dict
        :param materials: names of the sold items
        :type materials: list
        :param stock_actuel: current stock in the warehourses
        :type stock_actuel: dict

        :return: matrice_stock
        :rtype: dict
    """

    matrice_stock={}

    for element in materials:
        #Dispatch du produit "element" dans les 3 entrepots
        dispatch_element=[]
        for i in range (0,3):
            dispatch_theorique = prediction[element][i]
            if (dispatch_theorique * stock_actuel[element][3] > stock_actuel[element][i]):
                dispatch_element.append(floor(dispatch_theorique * stock_actuel[element][3] - stock_actuel[element][i]))
            else:
                dispatch_element.append(0)

        # Unites non reparties dans les entrepots secondaires
        reste = stock_actuel[element][3] - dispatch_element[0] - dispatch_element[1] - dispatch_element[2]

        reste_a_envoyer = []
        for i in range (0,3):
            dispatch_theorique = prediction[element][i]
            reste_a_envoyer.append(reste * dispatch_theorique)

        matrice_stock[element] = [floor(dispatch_element[i] + reste) for i,reste in enumerate(reste_a_envoyer)]

    print("matrice_stock ",matrice_stock)
  
    return(matrice_stock)


def getMatricePrix(ventes_veille, prix_actuels, frequence_reapro, jour_du_cycle, stock_actuel, materials, current_sim_elapsed_steps):
    """
        Give the prices modifications advices that must be applied in ERP Sim

        It returns a dict

        :param ventes_veille: sales from last days
        :type ventes_veille: dict
        :param prix_actuels: current prices for items
        :type prix_actuels: dict
        :param frequence_reapro: number of days between 2 main warehouse deliveries
        :type frequence_reapro: int
        :param jour_du_cycle: day since last main warahouse delivery
        :type jour_du_cycle: int
        :param stock_actuel: current stock in the warehourses
        :type stock_actuel: dict
        :param materials: names of the sold items
        :type materials: dict

        :return: dictionnaire_prix
        :rtype: dict
    """
    costPrices=getCostPrices(materials)
    jours_cycle_restants = frequence_reapro + 1 - jour_du_cycle

    dictionnaire_prix = {}

    for element in materials:
        if (ventes_veille[element][0] / current_sim_elapsed_steps >= stock_actuel[element][0]/jours_cycle_restants or ventes_veille[element][1] / current_sim_elapsed_steps >= stock_actuel[element][1]/jours_cycle_restants or ventes_veille[element][2] / current_sim_elapsed_steps >= stock_actuel[element][2]/jours_cycle_restants):
            dictionnaire_prix[element]=[1.1, str(round(1.1*prix_actuels[element], 2))+"€"]
        elif (ventes_veille[element][0] / current_sim_elapsed_steps < 0.8*stock_actuel[element][0]/jours_cycle_restants and ventes_veille[element][1] / current_sim_elapsed_steps < 0.8*stock_actuel[element][1]/jours_cycle_restants and ventes_veille[element][2] / current_sim_elapsed_steps < 0.8*stock_actuel[element][2]/jours_cycle_restants):
            if(costPrices[element]<round(0.9*prix_actuels[element])):
                dictionnaire_prix[element]=[0.9, str(round(0.9*prix_actuels[element], 2))+"€"]
            else:
                dictionnaire_prix[element]=[1, str(round(prix_actuels[element], 2))+"€"]
        else:
            dictionnaire_prix[element]=[1, str(round(prix_actuels[element], 2))+"€"]

    #insertDB(dictionnaire_prix, var.mydb)

    return dictionnaire_prix