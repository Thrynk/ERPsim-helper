Installation
============

.. note::
    Requierements – qu'est-ce qu’il faut installer ? Comment l’installer ? Comment lancer le projet ?  

.. _installation:

Language 
--------

This project is developped with Python Language, because it offers ...

Pour installer Python, rendez-vous sur le `site officiel <https://www.python.org/downloads/>`_ de Python. Pour information, ce projet a été développé avec Python 3.9.

Vous pouvez retrouver les différents :ref:`packages <packages>` utilisés ci-dessous.


.. _packages:

Packages
--------

To use ERPsim, first install it using pip:

.. code-block:: console

   (.venv) $ pip install ...

Les différents packages sont :

* Django (3.2.11)
* python-dotenv (0.19.2)
* python-dotenv[cli] (0.19.2)
* huey (2.4.3)
* redis (4.1.0)
* mysql-connector-python (8.0.26)
* pyodata (1.7.1)
* requests (2.23.0)

Tous ces packages sont dand le fichier *requierements.txt*
Pour tout installer en une fois, vous pouvez effectuer la commande suivante

.. code-block:: console

    (.venv) $ pip install -r requirements.txt

ou 

.. code-block:: console

    (.venv) $ pip3 install -r requirements.txt
