# install gcloud cli - follow these instructions! 
https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

if you have problems such as ...
do this:
curl https://dl.google.com/dl/cloudsdk/release/install_google_cloud_sdk.bash | bash
(from https://stackoverflow.com/questions/23247943/trouble-installing-google-cloud-sdk-in-ubuntu )

# deployment

## configure gcloud

    gcloud init
    
## deploy

    gcloud app deploy
    
beware: not immediate...
    

## view logs

    gcloud app logs tail -s default
