# SpaCyServer
This is a simple flask based rest service which can be run as docker container.
This is just to demo how spacy service would run on GKE.

## How to build the container
1. Clone the repository
2. Go the the root directory of clone.
3. Run `docker build -t spacy-server:1.0 .`

## Running the container

`
docker run -p 8050:8050 spacy-server:1.0

`

## Testing the endpoing

` 

curl -d '{"text":"This is a demo for running Spacy on GKE"}' -H "Content-Type: application/json" -X POST http://localhost:8050/extract-phrase
{"noun":["a demo","Spacy","GKE"],"verb":["running"]}

`

