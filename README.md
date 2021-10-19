# ERPsim-helper

This project aims to create an helper for ERPsim simulation game.

## Development

First, ask to have access to the Google Cloud project at **biprojectiseng1@gmail.com** .

### Accessing the MySQL database 

1. [Install MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
2. [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. Launch port forwarding with the Google Cloud :
```bash
gcloud compute ssh odata-db --project m2-project-329512 --zone us-east1-b -L 3306:localhost:3306
```
5. Setup MySQL Workbench connection :
![MySQL Workbench connection setup]()
