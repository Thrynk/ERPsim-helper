# IMPORTS 


# VARIABLES STATIQUES 
JEU_EN_COURS = True 


# DEFINITION DES FONCTIONS 
"""
Fonction extract_data_once qui prend en argument ......... 
Elle charge en une fois toutes les données du flux odata pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_once():
    print("Partie terminée. ")
    return True


"""
Fonction extract_data_loop qui prend en argument ......... 
Elle charge les (nouvelles) données du flux odata toutes les x secondes pour les sauvegarder dans la base de donnée MySQL
Retourne ..... 
"""
def extract_data_loop():
    print("Partie en cours...")
    return True


# MAIN 
if __name__ == "__main__" :
    # Demande si les données qui vont être chargées viennent d'une partie en cours ou d'une partie terminée. 
    JEU_EN_COURS = int(input("Vous chargez les données d'une partie (1)En cours ou d'une partie (2)Terminée ? ")) == 1

    # Lancement des fonctions en conséquence.
    if JEU_EN_COURS :
        extract_data_loop()
    else :
        extract_data_once()
