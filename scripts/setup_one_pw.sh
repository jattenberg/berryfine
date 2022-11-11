#!/bin/bash
# this sets up all the things you'd need to use the 1pw (`op`)
# command line client to manage this project
# usage: PG_UN=[postgres un] PG_PW=[postgres_pw] PG_URL=[postgres url] ./setup_one_pw.sh
# (configures the env vars used to store secrets)
VAULT="nba_app"
op vault create $VAULT
# note: i couldnt get this part to work
# todo: cli secret management
#op item create \
#    --category login \
#    --title "render posgres tt" \
#    --vault $VAULT \
#    --url $PG_URL \
#    --password $PG_PW \
#    --username $PG_UN
