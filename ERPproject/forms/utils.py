import pandas as pd
import mysql.connector

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
        host="localhost",
        user="odata",
        password="xGf#57PsB?td",
        port="3306"
    )
    return mydb


if __name__ == "__main__":
    print("Utils.py script for useful functions.")
