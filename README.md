# scrapping-notifications-service

Service to scrap the Federacio Catalana de Voleibol website (competicio.fcvoleibol.cat) in order to find the most recent games results and send email notifications to users.

Following this tutorial for managing cloud functions:
https://dev.to/googlecloud/moving-your-cron-job-to-the-cloud-with-google-cloud-functions-1ecp

and this for sending email part
https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server

To test your cloud-function locally:
pip install functions-framework
- export GOOGLE_APPLICATION_CREDENTIALS="path"
- export env variables
$ functions-framework --target my_function  (no .py)



GOOGLE CLOUD deployment

https://cloud.google.com/docs/authentication/getting-started


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

For the cron-job:
use google cloud scheduler tab