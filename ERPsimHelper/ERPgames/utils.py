import os
import pandas as pd
import mysql.connector


def getSalesData(mydb):
    cmd = str("SELECT row_number, sim_calendar_date, sales_organization, material_label, quantity, storage_location"
              " FROM sales")
    df = pd.read_sql(cmd, mydb)
    return df


def getInventoryData(mydb):
    cmd = str("SELECT row_number, sim_calendar_date, plant, storage_location, material_label, inventory_opening_balance"
              " FROM inventory")
    df = pd.read_sql(cmd, mydb)
    return df


def createDf(mydb, table):
    # Creation du cursor qui va pointer vers la collection
    Cursor = mydb.cursor(buffered=True)
    Cursor.execute("USE erpsim_games_flux")
    cmd = str("SELECT * FROM " + table)
    Cursor.execute(cmd)

    CursorName = mydb.cursor()
    CursorName.execute("USE erpsim_games_flux")
    cmd = str(
        "SELECT column_name FROM information_schema.columns WHERE table_schema='erpsim_games_flux' AND table_name='" + table + "'")
    CursorName.execute(cmd)

    df = cursorToCsv(Cursor, CursorName)
    return df


# Function to transform a cursor to a dataframe
def cursorToCsv(cursor, cursorName):
    liste = []
    column = []
    for x in cursor:
        liste.append(x)
    for y in cursorName:
        column.append(y[0])
    df = pd.DataFrame(liste, columns=column)
    return df


def dbConnexion():
    # Connection a la BDD SQL
    mydb = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE")
    )
    return mydb


if __name__ == "__main__":
    print("Utils.py script for useful functions.")
    mydb = dbConnexion()
    results = getSalesData(mydb)
    print(results)
