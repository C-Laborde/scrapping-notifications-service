# scrapping-notifications-service

Service to scrap the Federacio Catalana de Voleibol website (competicio.fcvoleibol.cat) in order to find out if
new games results have been uploaded and, if so, send an email notifications to users.

The service is deployed as a cloud function in google cloud and the jobs scheduler is used to
run a chron job every weekend to parse the website.

Following this tutorial for managing cloud functions:
https://dev.to/googlecloud/moving-your-cron-job-to-the-cloud-with-google-cloud-functions-1ecp

and this for sending email part:
https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server

LOCAL testing:
pip install functions-framework
- export GOOGLE_APPLICATION_CREDENTIALS="path"
- export env variables
$ functions-framework --target my_function  (no .py)



GOOGLE CLOUD deployment

https://cloud.google.com/docs/authentication/getting-started


gcloud init

(Without env vars)
gcloud functions deploy NAME --runtime python37 --trigger-http

With env vars (credentials are set as env vars so I need to declare them
during deployment)
gcloud functions deploy NAME --set-env-vars FOO=bar,BAZ=boo --runtime python37 --trigger-http
(No spaces between env vars)

TODO: load env var from yaml

(This gives an endpoint)
gcloud beta functions deploy test --runtime python37 --trigger-http
(to use beta functionality)

For the cron-job:
use google cloud scheduler tab