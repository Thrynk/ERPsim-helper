.. _difficultees:

========================
Difficultées rencontrées
========================

La complexité de SAP
--------------------

SAP, est difficile à comprendre pour un public non averti comme nous. |br|
Nous avions peu de temps pour réaliser la partie fonctionnel du projet, nous avions peu de marge de manoeuvre, nous permettant de faire des recherches sur SAP. |br|
Une grande partie de notre temps consacré à l'apprentissage de nouvelles connaissances a été dédié au jeu *ERPSIM*. |br|
Nous avons du jouer plusieurs parties afin de comprendre le mécanisme du jeu, mettre en évidence les :ref:`paramètres du jeu <paramètres_jeu>`. 
Nous avons aussi essayé de comprendre ce qui influençait la *company valuation* qui est ni plus ni moins que notre score sur le jeu en essayant différentes stratégies. 


Les simulations / Lancements des parties
----------------------------------------

Le projet, au stade initial, consistait à développer une Intelligence Artificielle (IA), capable de jouer à *ERPSIM* et de gagner ! 

Le problème : pour développer une IA il faut beaucoup de données. Soit des données de parties terminées jouées par des étudiants, ou, dans le cas échéant,
jouer, simuler des parties nous même pour engranger un maximum de données. 

Effectivement, nous ne pouvions pas utiliser les données des autres étudiants pour deux raisons : 

* Le jeu ne permet pas de garder en mémoire toutes les données de toutes les parties, le serveur doit être réinitialiser fréquemment.
* Ces derniers ne jouent pas exactement au même jeu que nous. 

En effet, le jeu propose plusieurs modes, Extended, Manufacturing, ou Introduction. Les étudiants jouent au jeu Manufacturing tandis que nous, nous 
développons avec le mode Introduction car ce dernier est bien plus simple à utiliser et à coder. Avec le temps que nous avions et nos connaissances sur SAP, 
ce mode était donc un bon compromis. 

Nous devions donc jouer des parties Introduction pour générer de la donnée mais nous avons été confronté à un autre problème : nous ne pouvons pas lancer de parties 
nous-mêmes et encore moins autant que nous le voulions. Nous devons, pour chaque partie, contacter un enseignant pour qu'il crée la partie avec ses identifiants administrateur 
sur *ERPSIM*. Il fallait donc que l'enseignant soit disponible au moment où nous voulions créer des parties, et qu'aucun cours de Serious Game ne soit en cours. 

Avec ces difficultées, nous avons pensé à reproduire le jeu pour faire des simulations nous-mêmes. Mais, entre le temps de développement de cette simulation, son utilisation, 
l'apprentissage de l'IA, ce procédé était tout bonnement impossible au vu du temps disponible pour le projet. 

C'est donc à ce moment que le projet d'IA, s'est transformé en programme d'aide pour le joueur. 

Difficultés techniques
----------------------

^^^^^^^^^^^^^^^^^^^^^^^^
Récupération des données
^^^^^^^^^^^^^^^^^^^^^^^^

Les principales difficultés nous ayant freinées dans le développement de la récupération des données :

* Pouvoir arrêter des tâches planifiées lorsque le professeur met une partie en pause, puis les ré-exécuter lorsqu'il décide de reprendre la partie. |br| Huey ne permet pas de faire ça, nous pouvons stopper les tâches planifiées mais lorsque nous les ré-exécuterons, le Scheduler les éxecutera car leur échéance d'exécution sera arrivée à terme (et nous ne pouvons pas re planifier ces tâches). |br| Il faut alors les stopper (avec Huey) puis sauvegarder les paramètres avec lesquels elles ont été lancé dans Redis puis de re-créer des nouvelles tâches avec ces paramètres lorsque le professeur relance la partie.
* Pour Django, créer un processus d'authentification personnalisé, utilisant les identifiants OData, nous a demandé d'effectuer des recherches et de mieux comprendre le fonctionnement de Django, et cela nous a pris du temps.

^^^^^^^^^
Affichage
^^^^^^^^^

* Passage de matplotlib à plotly pour des raisons de performance et pour ajouter de l'interactivité aux graphiques.

^^^^^^^^^^^^^^^^^^^^
Stratégie conseillée
^^^^^^^^^^^^^^^^^^^^

* Ne pas pouvoir directement tester la stratégie en direct avant d'avoir un système de récupération des données fiable.

**Lecture suivante**

Prochaine section : :doc:`PerspectivesEvolution`.