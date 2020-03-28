# scrapping-notifications-service

Service to scrap the Federacio Catalana de Voleibol website (competicio.fcvoleibol.cat) in order to find the most recent games results and send email notifications to users.

following this tutorial
https://dev.to/googlecloud/moving-your-cron-job-to-the-cloud-with-google-cloud-functions-1ecp

pip install functions-framework
$ functions-framework --target my_function



GOOGLE CLOUD deployment

https://cloud.google.com/docs/authentication/getting-started

- export GOOGLE_APPLICATION_CREDENTIALS="path"
- export env variables
gcloud init

Without env vars
gcloud functions deploy NAME --runtime python37 --trigger-http

With env vars:
gcloud functions deploy NAME --set-env-vars FOO=bar,BAZ=boo --runtime python37 --trigger-http
(No spaces between env vars)

TODO: load env var from yaml

(This gives an endpoint)
gcloud beta functions deploy test --runtime python37 --trigger-http
(to use beta functionality)