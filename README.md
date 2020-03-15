# scrapping-notifications-service

Service to scrap the Federacio Catalana de Voleibol website (competicio.fcvoleibol.cat) in order to find the most recent games results and send email notifications to users.

pip install functions-framework
$ functions-framework --target my_function



GOOGLE CLOUD deployment

https://cloud.google.com/docs/authentication/getting-started
- export GOOGLE_APPLICATION_CREDENTIALS="path"

gcloud init

gcloud functions deploy NAME --runtime python37 --trigger-http
