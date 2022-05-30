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

=> Trouver le prix d'équilibre entre garantir des ventes et maximiser le CA |br|
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

Cette stratégie nous a permis de conclure 3 choses. |br|
La première confirme le fait que les marchés sont bien indépendants entre les équipes. En effet, le jeu en mode Logistics Introduction, possède une option pour avoir un marché unique pour toutes les équipes ou un marché par équipe. Pour cette dernière option, il faut noter que les marchés de chaque équipe sont identiques, seulement si l'équipe A vend beaucoup, l'équipe B peut aussi vendre beaucoup. Les ventes ne sont pas réparties entre les équipes, contrairement à la première option. 

Ce choix avait été fait pour faciliter la compréhension du jeu dans un premier temps. 

La deuxième conclusion à tirer de cette expérience, est qu'un produit, à un prix donné, ne se vend pas du tout de la même manière en fonction des jours 
même si aucun paramètre ne change (prix ou stock). Cette fluctuation est donc à prendre en compte pour notre stratégie finale afin de conseiller le joueur 
non pas sur ses ventes de la veille, mais sur les ventes des jours précédents. Le nombre de jours de ventes à prendre en compte dans la stratégie reste à
définir. 

La troisième conclusion : il faut éviter d'avoir trop de stocks et de tomber en rupture de stock, car on ne fait plus de profit, la Company Valuation chutte alors fortement.

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
Nous calculons alors la quantité de ventes du produit dans la région puis le divisons par 
la quantité de ventes de ce produit dans toutes les régions, 
ce qui nous donne une proportion de ventes pour chaque région Nord, Sud et Ouest.

:math:`proportion \, des \, ventes \, de \, p \, dans \, la \, région \, r = \frac{ventes_{p,r}}{ventes_{p}} = \% \, ventes_{p,r}`

Avec :

* :math:`p` : Le produit
* :math:`r` : La région

Cette proportion nous aide à savoir combien envoyer dans chaque région pour chaque produit.

Calcul de la quantité à envoyer dans chaque région
""""""""""""""""""""""""""""""""""""""""""""""""""

Nous calculons ensuite, combien envoyer de l'entrepôt principal aux entrepôts régionaux de la manière suivante : |br|

:math:`\forall p \in produits\quad \forall r \in régions`

Si
    :math:`\% \, ventes_{p,r} * stock_{p,entrepôt \, principal} > stock_{p,r}`

Alors
    On envoie :math:`\% \, ventes_{p,r} * stock_{p,entrepôt \, principal} - stock_{p,r}`

Sinon
    :math:`0` : Nous n'envoyons rien car nous avons assez de stock dans l'entrepôt régional.
    Les entrepôts régionaux qui sont plus dans le besoin seront grâce à cela, plus réapprovisionnés que celui-ci.

:math:`\forall p \in produits`

    Nous envoyons le reste du stock de l'entrepôt principal en le dispatchant proportionnellement à :math:`\% \, ventes_{p,r}`

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

**Si** le nombre moyen de ventes par jour > au stock restant par jour jusqu'au prochain réapprovisionnement
    
    On augmente le prix de 10%.

**Sinon si** le nombre moyen de ventes par jour < 80% du stock restant par jour restant avant le prochain réapprovisionnement, nous ne vendons pas assez

    **Alors si** 0.9 * le prix actuel du produit > prix de revient

        Nous baissons le prix de 10% pour vendre plus.

    **Sinon**

        Nous ne baissons pas le prix pour ne pas vendre à perte.

**Sinon**

    Nous laissons les prix actuels.

Nous avons fixé à 10% dans un premier temps pour simplifier la complexité du problème, et pour simplifier les manipulations du joueur. |br|
Une amélioration possible de la stratégie serait de trouver une méthode pour estimer ce pourcentage, avec par exemple les NPS Surveys.
