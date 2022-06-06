.. _deploiement:

Déploiement
===========

^^^^^^^^^^^^^^
Linux - Debian
^^^^^^^^^^^^^^

Si vous souhaitez déployer le projet sur une machine Linux, il vous faudra installer :

    * Docker
    * Docker Compose

Installation de Docker et Docker Compose
""""""""""""""""""""""""""""""""""""""""

Pour installer sur Debian, suivez le tutoriel `ici <https://docs.docker.com/engine/install/debian/>`_.

Si vous êtes sur un autre Linux, cherchez comment installer Docker et Docker Compose.

Cloner le repository Github
"""""""""""""""""""""""""""

.. code-block:: console
    
    git clone https://github.com/Thrynk/ERPsim-helper.git && cd ERPsim-helper

Lancer les conteneurs Docker
""""""""""""""""""""""""""""

.. code-block:: console

    docker compose up -f docker-compose.prod.yml