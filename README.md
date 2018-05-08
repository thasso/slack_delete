# Slack File Delete

This repo contains a script to delete your local users files. Either all of them or filtered by age.

The script requires a slack token generated with your user. Go to https://api.slack.com/custom-integrations/legacy-tokens to get or create such token.

## Run with local python

To run this script on your machine, make sure you install the dependencies first, best within a virtual environment:

    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
    ./slack_delete.py -t <token> -d 30

The command above assumes that python 3.x is your default python (tested with 3.6) and that you have virtualenv installed.

## Run with Docker

The repo contains a Dockerfile that you can use for your convenience:

    docker build -t slack_delete .
    docker run --rm -ti slack_delete -t <token> -d 30

# Credits

The script is a slighlyt modified version of https://gist.github.com/jackcarter/d86808449f0d95060a40