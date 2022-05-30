# ERPsim-helper

This project aims to create an helper for ERPsim simulation game.

## Development

First, ask to have access to the Google Cloud project at **biprojectiseng1@gmail.com** .

### Accessing the MySQL database 

#### Installation setup

1. [Install MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
    - MySQL Workbench requires the following installation (try to install them if direct install is not working) :
        - ![MySQL Workbench Wizard](/docs/img/mysql-workbench-wizard.png)
            1. Click on Donwload Prerequisites.
            2. Go to the requirements information ![MySQL Workbench Requirements Info](mysql-workbench-requirements-info.png)
        - Install [.NET framework 4.5 requirement](https://www.microsoft.com/en-us/download/confirmation.aspx?id=30653)
        - [Microsoft Visual C++ Redistributable for Visual Studio 2019](https://visualstudio.microsoft.com/fr/downloads/?q=Visual+C%2B%2B+Redistributable+for+Visual+Studio+2019). Install it if you don't have it.
        ![Visual Studio download](/docs/img/redistribuable-download.png)
2. [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. Add IAM policy binding to service account user in google cloud (ask project owner)
```bash
gcloud projects add-iam-policy-binding m2-project-329512 --member="user:test-user@gmail.com" --role="roles/iam.serviceAccountUser"
```

#### Connect to database

1. Launch port forwarding with the Google Cloud :
```bash
gcloud compute ssh odata --project m2-project-329512 --zone us-east1-b -- -L 3306:localhost:3306
```
2. You can either :
    1. Connect via the mysql client on the Compute Engine instance
    ```bash
    mysql -u odata -p
    ```
    2. Setup MySQL Workbench connection :
    ![MySQL Workbench connection setup](/docs/img/manage-server-connections.png)
    3. use MySQL VS code extension :
    ![MySQL vscode extension](/docs/img/mysql-vscode-extension.png)

#### To do

Récupérer les données :
- Installation de mysql sur Compute Engine (Done)
- Installation de MySQL Workbench
- Lister les données intéressantes à récupérer
- Créer les schémas des données
- Récupérer à l'aide d'un programme python les données de flux odata
    - Choisir le service Cloud permettant de faire ça
    - Réaliser le code pour récupérer une partie finie
    - Réaliser le code pour récupérer en streaming

### Install the website server

### Understand the algorithm
