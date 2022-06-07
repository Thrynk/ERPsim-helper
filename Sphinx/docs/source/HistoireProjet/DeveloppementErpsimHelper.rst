.. _developpement-erpsim-helper:

==========================================
Développement de la solution ERPSIM Helper
==========================================

Répartition des tâches
----------------------

Pour réaliser le programme du projet, nous nous sommes répartis en 3 groupes : 

* Une partie pour l'extraction des données brutes 
* Une partie création d'une stratégie et réalisation des dashboard de visualisation 
* Une partie création des formulaires administrateur et player. 

Les différentes parties de ce projet ont été crées sur un `GitHub <https://github.com/Thrynk/ERPsim-helper>`_. 

Critères de récupération du flux oData 
--------------------------------------

La récupération des données est une étape indispensable pour réaliser notre aide. Nous avons donc réaliser un découpage en fonctions 
principales et fonctions contraintes afin de développer cette extraction de la meilleure des manières. 

* FP 1 : Extraire les données du flux oData 
* FP 2 : Stocker les données dans une base de données (afin de pouvoir analyser les parties une fois jouées sans être impacté par les changements de scénario du professeur). 

* FC 1 : L'authentification du joueur doit se faire avec ses identifiants ERPSIM pour se connecter au flux oData
* FC 2 : Le rechargement doit s'opérer de manière automatique 
    * FC 2.1 : Les rechargements doivent se faire jusqu'à la fin de la partie, quelque soit la durée de la partie 
    * FC 2.2 : Les rechargements doivent se mettre en pause si l'enseignant met en pause la partie
    * FC 2.3 : Les rechargements doivent se remettre en marche quand l'enseignant relance la partie après une pause 
    * FC 2.3 : Les rechargements doivent s'arrêter si on atteint le Jour 10 du Round 8
* FC 3 : Le processus d'extraction et de stockage des données doit prendre moins d'une minute. 
* FC 4 : La base de données doit être disponible le plus longtemps possible

^^^^^^^^^^^^^^^^^^^^
Choix architecturaux
^^^^^^^^^^^^^^^^^^^^

Une fois les données stockées, nous devons les contextualiser par partie, et associer l'utilisateur aux données de sa partie. |br|
Nous avons pour cela, décidé d'utiliser Django Server. |br| 
En effet, les modèles Django permettent de créer des tables dans une base de données, et de les alimenter. Django permet aussi, de gérer l'authentification des utilisateurs via un formulaire personnalisable.

En plus de Django, nous avons utilisé `Huey <https://huey.readthedocs.io/en/latest/>`_. |br|
Cette bibliothèque, s'associant avec Django, permet de créer des tâches de rechargements planifiées. |br| 
Nous pouvions grâce à cela, créer les tâches de rechargements pour chaque table du flux, et les lancer en parralèle, avec du multi-threading, de manière à augmenter la rapidité de l'extraction. |br|
Huey nous permet aussi de `scheduler` les tâches, pour les exécuter tous les :math:`x` minutes. |br|
Huey, pour stocker les tâches utilise `Redis <https://redis.io/>`_. |br|

Pour stocker les données, nous avons choisi d'utiliser une base MySQL, qui est utilisable avec Python grâce à la librarie `mysql-connector-python <https://dev.mysql.com/doc/connector-python/en/>`_. |br|
MySQL est une base relationnelle avec laquelle nous avons des connaissances et permettant de stocker des données tabulaires relationnelles comme les données venant du flux OData.

Enfin, pour extraire les données du flux oData, nous avons utilisé la librairie `pyodata <https://github.com/SAP/python-pyodata>`_, nous permettant de faire des requêtes au flux OData simplement.

Cette solution nous permet de mettre en place la synchronisation avec le flux OData, dans les temps impartis afin de pouvoir rapidement tester la stratégie.

Critères pour l'affichage des graphiques
----------------------------------------

Pour la partie affichage des graphiques, 

* FP 1 : Afficher l'évolution des stocks de l'entrepôt général ainsi que des entrepôts régionaux
* FP 2 : Afficher les ventes de chaque produit pour chaque région
* FP 3 : Afficher un tableau décrivant comment répartir les stocks de l'entrepôt principal
* FP 4 : Afficher un tableau décrivant comment modifier les prix des produits 

* FC 1 : La page ne doit pas s'alourdir au fil des Jours
* FC 2 : La page doit se rafraîchir en moins de 10 secondes
* FC 3 : La page ne doit pas "ne pas répondre" pendant l'actualisation des données

^^^^^^^^^^^^^^^^^^^^
Choix architecturaux
^^^^^^^^^^^^^^^^^^^^

Nous avons décidé d'utiliser la librairie `plotly <https://plotly.com/>`_ afin de créer des graphiques interactifs en Python puis de les envoyer depuis Django au navigateur Web. |br|
Cette librairie open-source nous permet d'afficher des graphiques qui puissent être intéractifs afin de pouvoir filtrer par produit car nos graphiques risquaient d'être chargés si nous n'avions pas la possibilité de filtrer par produit. |br|
Elle s'intègre également facilement avec Django et Pandas (nous permettant de faire des calculs facilement sur les données).

Critères pour la stratégie conseillée
-------------------------------------

* FP 1 : La stratégie doit permettre au joueur d'avoir une meilleure Company Valuation

* FC 1 : La stratégie ne doit pas faire vendre à perte
* FC 2 : La stratégie doit limiter au maximum les ruptures de stocks 
* FC 3 : La stratégie doit adapter le stock dans les entrepôts régionaux en fonction des ventes de chaque région 
* FC 4 : Le calcul de la stratégie doit prendre moins de 30 secondes

^^^^^^^^^^^^^^^^^^^^
Choix architecturaux
^^^^^^^^^^^^^^^^^^^^

Pour la stratégie, nous avons décidé d'utiliser la librairie Pandas afin de pouvoir effectuer nos calculs facilement sur les données de la partie.


**Lecture suivante**

Prochaine section : :doc:`ResultatsProjet`.