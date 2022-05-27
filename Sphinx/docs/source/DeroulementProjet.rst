.. _bilan_projet:

Histoire du Projet
==================

===================
Démarrage du projet 
===================

Le but du projet était de créer une Intelligence Artificielle capable de jouer et de gagner à *ERPSIM*. 

Pour ce faire, nous avons lu et mis de côté les informations importantes des guides d'utilisation fournis par HEC Montréal 
afin de faire un condensé des informations à retenir. Nous avons aussi joués plusieurs parties, pour se familiariser au 
fonctionnement du jeu, pour voir quelles données étaient présentes sur l'interface du jeu, mais aussi pour voir de quoi était 
composé le flux oData. En effet, le flux oData est le flux sur lequel nous extrayons les données. 

Etat de l'Art
-------------

.. _paramètres_jeu:

Les paramètres du jeu 
---------------------

Nous avons répertoriés les paramètres du jeu. Nous savons que nous pouvons agir sur les prix, les flux de transferts. En agissant sur ces derniers, 
nous influons les ventes et les stocks : 

.. figure:: _static/img/ParamètresERPSIM.png
    :align: center 
    :target: ../_images/ParamètresERPSIM.png

    *Liste des paramètres d'entrées et de sortie du jeu ERPSIM*

============================
Construction de la stratégie
============================

Nous avons alors commencé à élaborer des stratégies, dans le but de comprendre le fonctionnement du jeu, les paramètres essentiels pour 
avoir une bonne *company valuation* et donc un bon score. 

Stratégie de découverte : La stratégie du produit unique
--------------------------------------------------------

L'une d'elles consistait à se contenter d'un seul produit. Nous sommes 7 dans le groupe, nous avons donc joué à 6, et une personne
centralisait tout. Nous étions chacun affecté à un seul et unique produit, nous ne devions toucher à aucun autre produit, que ce soit
pour le stock ou pour le prix. Le but de cette manipulation était de comprendre comment les produits se vendaient. Nous essayions aussi
dans la limite du possible, de ne pas changer de prix trop régulièrement de manière à voir si les ventes variaient avec un prix fixe
ou non. 

^^^^^^^^^^^^^^^^^^^^^^^
Stratégie mise en place 
^^^^^^^^^^^^^^^^^^^^^^^

* Saturation des dépôts : On ne doit pas avoir de rupture de stock
* Modifications jour par jour des prix des produits et observation de l'impact sur les ventes

^^^^^^^^^
Objectifs 
^^^^^^^^^

1. 12 000 € de Chiffre d'affaire / Jour 
2. Maximiser les ventes par produit 

=> Trouver le prix d'équilibre entre garantir des ventes et maximiser le CA 

=> Optimiser :math:`y(p) = x(p) * q(p)` 

avec 

* :math:`y(p)` Le chiffre d'affaire par produit 
* :math:`x(p)` Le prix du produit 
* :math:`q(p)` La quantité vendue du produit 

^^^^^^^^^^^^^^^
Mode opératoire 
^^^^^^^^^^^^^^^

* Rounds 1 à 4 : 
    * Augmenter de 60 % le prix de tous les produits sauf le sien
    * Chacun devra relever jour par jour le prix et le nombre de ventes de son produit 
    * Si le produit :math:`x(p) * q(p)` est supérieur à la veille : 
        * réitérer la dernière variation de prix
        * sinon faire l'inverse de façon plus progressive 
    * ATTENTION, il faut faire le nécessaire pour que les dépôts ne soient jamais vides pour le produit que l'on étudie
        * Si nécessaire, la capacité des dépôts peut être excédée
    * A la fin des 4 rounds, mise en commun
* Round 5 : 
    * Chacun va adapter ses prix avec les prix d'équilibre trouvés par les autres équipes, cela permettra, en observant les données oData, de savoir si le marché est bien indépendant des autres. 

^^^^^^^^^^
Conclusion
^^^^^^^^^^

Cette stratégie nous a permis de conclure 2 choses. La première confirme le fait que les marchés sont bien indépendants entre les équipes. En effet,
le jeu en mode Logistic Introduction, possède une option pour avoir un marché unique pour toutes les équipes ou un marché par équipe. Pour cette dernière
option, il faut noter que les marchés de chaque équipe sont identiques, seulement si l'équipe A vend beaucoup, l'équipe B peut aussi vendre beaucoup. Les ventes ne sont pas
réparties entre les équipes, contrairement à la première option. 

Ce choix avait été fait pour faciliter la compréhension du jeu dans un premier temps. 

La deuxième conclusion à tirer de cette expérience, est qu'un produit, à un prix donné, ne se vend pas du tout de la même manière en fonction des jours 
même si aucun paramètre ne change (prix ou stock). Cette fluctuation est donc à prendre en compte pour notre stratégie finale afin de conseiller le joueur 
non pas sur ses ventes de la veille, mais sur les ventes des jours précédents. Le nombre de jours de ventes à prendre en compte dans la stratégie reste à
définir. 

Stratégie d'ERPSIM Helper
-------------------------

La stratégie doit générer 2 tableaux permettant à l'utilisateur de savoir 
quelles actions effectuer sur les 2 paramètres modifiables du scénario Logistics Introduction du jeu ERPSIM :

* Un tableau retournant l'information de la quantité de stock à envoyer dans chaque entrepôt pour chaque produit
* Un autre tableau nous disant à quel prix vendre chaque produit

L'aide ERPSIM helper retranscrira également les aides sous forme de phrases aidant le joueur à interpréter ces tableaux.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Calcul de la prédiction des stocks à envoyer dans chaque région
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Répartition des ventes
""""""""""""""""""""""

Afin de savoir quelle quantité de chaque produit envoyer dans chaque entrepôt, nous devons nous baser sur la demande Client. |br|
L'information nous permettant de déduire quelle est la demande pour chaque produit, est l'historique des ventes. |br|
Nous calculons alors la quantité de ventes du produit dans la région puis le divisions par 
la quantité de ventes de ce produit dans toutes les régions, 
ce qui nous donne une proportion de ventes pour chaque région Nord, Sud et Ouest.

:math:`proportion \, des \, ventes \, de \, p \, dans \, la \, région \, r = \frac{ventes_{p,r}}{ventes_{p}}`

Avec :

* :math:`p` : Le produit
* :math:`r` : La région

Cette proportion nous aide à savoir combien envoyer dans chaque région pour chaque produit.

Calcul de la quantité à envoyer dans chaque région
""""""""""""""""""""""""""""""""""""""""""""""""""

Nous calculons ensuite, combien envoyer de l'entrepôt principal aux entrepôts régionaux de la manière suivante : |br|

:math:`\forall p \in produits\quad \forall r \in régions`

Si
    :math:`ventes_{p,r} * stock_{p,entrepôt \, principal} > stock_{p,r}`

Sinon
    :math:`0` : Nous n'envoyons rien car nous avons assez de stock dans l'entrepôt régional.
    Les entrepôts régionaux qui sont plus dans le besoin seront grâce à cela, plus réapprovisionnés que celui-ci.

:math:`\forall p \in produits`

    Nous envoyons le reste du stock de l'entrepôt principal en le dispatchant proportionnellement à :math:`ventes_{p,r}`

Cette stratégie permet d'envoyer le nombre de produits dans chaque région proportionnellement à la demande dans chacune de celles-ci.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Calcul du prix à appliquer pour chaque produit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nous utilisons pour calculer cela :

* Les ventes passées afin de savoir combien nous vendons par jour en moyenne
* Les prix actuels, pour savoir à combien, nous vendons actuellement nos produits
* La fréquence de réapprovisionnement du scénario (5 par défaut pour le scénario Logistics Introduction) et le jour courant dans ce cycle permettant de calculer le nombre de jours restants avant le prochain réapprovisionnement.
* Les stocks actuels

:math:`\forall p \in produits\quad \forall r \in régions`

**Si** le nombre moyen de ventes par jour > au stock restant par jour restant avant le prochain réapprovisionnement

    On augmente le prix de 10%.

**Sinon si** le nombre moyen de ventes par jour < 80% du stock restant par jour restant avant le prochain réapprovisionnement, nous ne vendons pas assez

    **Alors si** 0.9 * le prix actuel du produit > prix de revient

        Nous ne baissons pas le prix pour ne pas vendre à perte.

    **Sinon**

        Nous baissons le prix de 10% pour vendre plus.

**Sinon**

    Nous ne laissons les prix actuels.

Nous avons fixé à 10% dans un premier temps pour simplifier la complexité du problème, et pour simplifier les manipulations du joueur. |br|
Une amélioration possible de la stratégie serait de trouver une méthode pour estimer ce pourcentage, avec par exemple les NPS Surveys.

.. _resultats:

====================================
Résultats et Analyse de la stratégie
====================================

Les bénéfices pour l'utilisateur
--------------------------------

D'un point de vue visuel, nous pouvons trouver, sur :ref:`l'interface utilisateur <joueur>`, des conseils sur les prix, les transferts de stocks, et une vue plus générale 
de l'état de l'entreprise au premier coup d'oeil. Cette vue permet de prendre des décisions plus rapidement puisque toutes les informations sont centralisées.

D'un point de vue contenu, nous pouvons changer très rapidement les transferts de Stocks grâce au tableau présent en bas à gauche de la page 
car les lignes des produits sont dans le même ordre que dans le jeu, ainsi que les colonnes pour les régions. De ce fait, le joueur n'a plus 
qu'à recopier les valeurs présentes dans ce tableau. 

De la même manière, le tableau des prix, en bas à droite de la page, permet d'adapter les prix au plus vite. Attention toutefois à la latence 
qu'il peut y avoir entre ERPSIM et ERPSIM Helper. En effet, le temps que les données soient récupérées et affichées sur l'interface, il se peut 
qu'un jour soit passé sur ERPSIM. Il faut donc bien vérifier sur ERPSIM Helper, le Round et le Jour en cours, de manière à pas changer le prix 
deux fois. 

Méthode d'évaluation
--------------------



Résultats finaux
----------------

En termes de Company Valuation, nous pouvons voir ci-dessous, que cette dernière monte très vite au départ puis se stabilise à une bonne valeur. 

.. figure:: _static/img/Game48-CompanyValuation.png
    :align: center
    :target: ../_images/Game48-CompanyValuation.png

    *Company Valuation d'une partie jouée avec ERPSIM Helper*

On y voit donc que nous atteignons 1 million de Company Valuation au Jour 4 du Round 2, et nous ne repassons plus jamais en dessous dans le reste de 
la partie. Au terme de la partie, nous réussissons à avoir 1.47 millions de Company Valuation avec un pic à 1.49 millions au jour 8 du Round 8. 

Par rapport aux autres parties que nous avons pu jouer au cours de ce projet, c'est largement cette partie qui a été la mieux jouée avec la 
meilleure Company Valuation. Notre aide paraît donc fiable. 

Qui plus est, nous avons comparé notre score aux parties des étudiants de `Junia ISA <https://www.isa-lille.fr/isa-lille/>`_. Nous sommes bien conscients
que nous jouons à ERPSIM avec le scénario Logistics Introduction et que les autres étudiants jouent au scénario Extended et que la difficulté n'est pas 
la même, mais nous arrivons, avec ce score, à nous placer 3ème du classement. 

Ce dernier résultat est vraiment à prendre avec précaution, le calcul de la Company Valuation n'est pas le même dans ces deux scénarios. De plus, 
nous ne savons pas si la Company Valuation est "plafonnée" par un jeu parfait, qui pourrait différer en fonction des variables initiales de la partie. 
Cette remarque est donc là pour information, plus que pour montrer l'intérêt de notre solution.

Analyse de la stratégie
-----------------------

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
* FP 2 : Stocker les données dans une base de données 

* FC 1 : L'authentification du joueur doit se faire avec ses identifiants ERPSIM pour se connecter au flux oData
* FC 2 : Le rechargement doit s'opérer de manière automatique 
    * FC 2.1 : Les rechargements doivent se faire jusqu'à la fin de la partie, quelque soit la durée de la partie 
    * FC 2.2 : Les rechargements doivent se mettre en pause si l'enseignant met en pause la partie
    * FC 2.3 : Les rechargements doivent se remettre en marche quand l'enseignant relance la partie après une pause 
    * FC 2.3 : Les rechargements doivent s'arrêter si on atteint le Jour 10 du Round 8
* FC 3 : Le processus d'extraction et de stockage des données doit prendre moins d'une minute. 
* FC 4 : La base de données doit être disponible le plus longtemps possible

Connaissant l'objectif et les contraintes de cette partie, nous avons décidé d'utiliser Django Server. En effet, les modèles Django 
permettent de créer des tables dans une base de données, et de les alimenter. Django permet aussi, de gérer l'authentification des utilisateurs 
via un formulaire personnalisable. Cet outil nous permettait donc de gérer presque l'ensemble de cette partie extraction. 

En plus de Django, nous avons utilisé `Huey <https://huey.readthedocs.io/en/latest/>`_. Cette bibliothèque, permet de créer des `tasks`, utiles 
pour les tâches de rechargements. Nous pouvions grâce à cela, créer les tâches de rechargements pour chaque table du flux, et les lancer en 
parralèle, avec du multi-threading, de manière à augmenter la rapidité de l'extraction. Huey nous permet aussi de `scheduler` les tâches, pour 
les exécuter tous les :math:`x` minutes. Huey, pour stocker les tâches utilise `Redis <https://redis.io/>_`.

Pour stocker les données, nous avons choisi d'utiliser une base MySQL, qui est utilisable avec Python grâce à la 
libraie `mysql-connector-python <https://dev.mysql.com/doc/connector-python/en/>`_.

Enfin, pour extraire les données du flux oData, nous avons utilisé la librairie `pyodata <https://github.com/SAP/python-pyodata>`_. 

Critères pour l'affichage des graphiques
----------------------------------------

Pour la partie affichage des graphiques, 

* FP 1 : Afficher l'évolution des stocks de l'entrepôt général ainsi que des entrepôts régionaux
* FP 2 : Afficher les ventes de chaque produit pour chaque région
* FP 3 : Afficher un tableau décrivant comment répartir les stocks de l'entrepôt principal
* FP 4 : Afficher un tableau décrivant comment modifier les prix des produits 
* FP 5 : Afficher des *tips*, sous forme de phrase pour condenser les actions que le joueur doit faire

* FC 1 : La page ne doit pas s'alourdir au fil des Jours
* FC 2 : La page doit se rafraîchir en moins de 10 secondes
* FC 3 : La page ne doit pas "ne pas répondre" pendant l'actualisation des données

Critères pour la stratégie conseillée
-------------------------------------

* FP 1 : La stratégie doit permettre au joueur d'avoir une meilleure Company Valuation

* FC 1 : La stratégie ne doit pas faire vendre à perte
* FC 2 : La stratégie doit limiter au maximum les ruptures de stocks 
* FC 3 : La stratégie doit adapter le stock dans les entrepôts régionaux en fonction des ventes de chaque région 
* FC 4 : Le calcul de la stratégie doit prendre moins de 30 secondes

.. _difficultees:

========================
Difficultées rencontrées
========================

La complexité de SAP
--------------------

D'une manière générale, *ERPSIM*, et donc SAP, sont assez difficiles à comprendre pour un public non averti comme nous. 
En effet, nous avons du jouer plusieurs parties afin de comprendre le mécanisme du jeu, mettre en évidence les :ref:`paramètres du jeu <paramètres_jeu>`. 
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

.. _evolution:

========================
Perspectives d'évolution
========================

Interaction avec le jeu 
-----------------------

Actuellement, le joueur, s'il suit tous nos conseils, se contente juste de reproduire ce qu'on lui dit de faire. 
Il reproduit sur le *serious game* les indicateurs que nous lui communiquons. Pour palier à cette situation, il serait possible, 
avec `Selenium <https://selenium-python.readthedocs.io/>`_, d'intéragir sur la plateforme du *serious game* directement. 

En effet, si nous paramétrons correctement tous les boutons et champs utiles du jeu, nous pourrions écrire un programme 
qui clique et remplit les champs en fonctions des sorties de notre programme actuel. Cela faciliterait donc la tâche du joueur. 

Notre programme pourrait alors, ne plus petre considéré comme une aide mais jouer tel un BOT. 

.. warning:: 

    Attention toutefois, il suffirait d'un petit changement sur la plateforme du jeu pour ce code ne soit plus fonctionnel. 
    Cette fonctionnalité aurait donc des limites très précoces. 

Pour le mieux, il faudrait pouvoir executer les transactions directement sur le jeux comme elles sont faites sur les 
navigateurs quand nous cliquons ou remplissons les champs. Après des recherches à ce propos, nous n'avons rien trouvé de probant,
qui plus est, dans le temps limite consacré au développement de notre projet. 

Il faudrait de plus amples connaissances sur SAP, pour évoquer cette éventualité. 


Faciliter la vue du joueur
--------------------------

Dans le jeu, chaue joueur possède un rôle, une fonction, il peut gérer les stocks, les prix, les approvisionnements, ... 

Dans cette version de notre projet, les conseils sont donnés dans l'encadré en haut de page mais ne sont pas filtrés. 
On pourrait alors imaginer un système pour soit 

* Colorer les *tips* avec une couleur par rôle pour voir d'un seul coup d'oeil les conseils qui nous sont propres. 
* Avoir des boutons en haut de page, où nous pourrions filtrer les *tips* nous cernant, en masquant les *tips* des autres domaines du jeu. 

L'actualisation de l'interface du joueur 
----------------------------------------

Bien que les données soient récupérées du flux odata toutes les minutes de manière autonome, la page du joueur quant à elle 
n'est pas rafraîchie chaque minute : il faut cliquer sur `F5` ou sur le logo de rafraîchissement du navigateur pour voir les données 
et les graphiques s'actualiser. 

Nous pourrions donc prévoir un rechargement automatique de cette page afin que l'utilisateur n'ait pas besoin de le faire manuellement. 

Toutefois, pour limiter les risques, nous affichons clairement en grand, le *round* et le *day* en haut de page. De cette façon 
le joueur peut comparer ces valeurs à celles de l'interface du *Serious Game* pour savoir si les données présentées sont les dernières données. 

.. warning::

    Attention, sur l'interface du *Serious Game*, il faut aussi rafraîchir à la main le dashboard, les données ne sont pas actualisées
    automatiquement.

La robustesse de l'extraction des données
-----------------------------------------

