# scrapping-notifications-service

Service to scrap the Federacio Catalana de Voleibol website (competicio.fcvoleibol.cat) in order to find out if
new games results have been uploaded and, if so, send an email notifications to users.

The service is deployed as a cloud function in google cloud and the jobs scheduler is used to
run a chron job every weekend to parse the website.

I am following this tutorial for managing cloud functions:
https://dev.to/googlecloud/moving-your-cron-job-to-the-cloud-with-google-cloud-functions-1ecp

and this one for sending email part:
https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server

LOCAL testing:
pip install functions-framework
- export GOOGLE_APPLICATION_CREDENTIALS="path"
- export env variables (email sender variables)
- functions-framework --target my_function  (no .py)
- on a different command line: curl http://0.0.0.0:8080



GOOGLE CLOUD deployment

You will have to install Cloud SDK as explained here:
https://cloud.google.com/sdk/docs/quickstart


https://cloud.google.com/docs/authentication/getting-started

Start the console in the project where you want to deploy your cloud function:
- gcloud init

(Without env vars)
- gcloud functions deploy NAME --runtime python37 --trigger-http

With env vars (credentials are set as env vars so I need to declare them
during deployment)
- gcloud functions deploy NAME --set-env-vars FOO=bar,BAZ=boo --runtime python37 --trigger-http
(No spaces between env vars)

OBS: This may raise an error:
"ERROR: (gcloud.functions.deploy) OperationError: code=7, message=Build failed:
Cloud Build API has not been used in project XXXX before or it is disabled.
Enable it by visiting https://console.developers.google.com/apis/api/cloudbuild.googleapis.com/overview?project=XXXX
then retry. If you enabled this API recently, wait a few minutes for the action
to propagate to our systems and retry.
"
If you follow the link you will be able to enable the API.

A successful deployment will create an endpoint to execute the function.
The name of the endpoint is printed in the command line when the function is
deployed. It usually looks something like (don't click, this is a fake link):
https://us-central1-your-project-id.cloudfunctions.net/funcion-name

TODO: load env var from yaml

(This gives an endpoint)
gcloud beta functions deploy test --runtime python37 --trigger-http
(to use beta functionality)

For the cron-job:
use google cloud scheduler tab