#!/usr/bin/env bash


#########################
# The command line help #
#########################
USAGE="
Usage:
    sh deployment.sh CLUSTER_NAME PROJECT_NAME
Example:
    sh deployment.sh spacy-demo-cluster k8scaleio"
case $1 in
 -h) echo "$USAGE\n"; exit 0 ;;
  h) echo "$USAGE\n"; exit 0 ;;
  help) echo "$USAGE\n"; exit 0 ;;
esac

CLUSTER_NAME=$1
PROJECT_NAME=$2

gcloud container clusters get-credentials $CLUSTER_NAME

echo "Current context\n"
kubectl config current-context

DATE=`date '+%Y-%m-%d-%H-%M'`
RELEASE_TAG="RELEASE-"$DATE
echo "Releaseing:: "$RELEASE_TAG
docker build -t spacy-server:$RELEASE_TAG .
docker tag spacy-server:$RELEASE_TAG gcr.io/$PROJECT_NAME/spacy-server:$RELEASE_TAG
### Push the image to gcr
docker push gcr.io/$PROJECT_NAME/spacy-server:$RELEASE_TAG
DEPLOYMENT_FILE=spacy-server.yaml
echo $DEPLOYMENT_FILE
sed -i "s,RELEASE_TAG,$RELEASE_TAG,g" $DEPLOYMENT_FILE

### Apply to prod cluster
kubectl apply -f $DEPLOYMENT_FILE

## Restore the deployment file
sed -i "s,$RELEASE_TAG,RELEASE_TAG,g" $DEPLOYMENT_FILE

### get pods
kubectl get pods

