#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

if [[ $# -ne 1 ]]; then
    echo "Must specify either dev or prod"
    echo "USAGE: $0 [dev|prod]"
    exit 1
fi

if [ "$1" == "dev" ]; then
    APP=bcorps-hippo-backend-staging
else
    APP=bcorps-hippo-backend
fi

heroku config:set -a $APP GOOGLE_SERVICE_ACCT_KEY="$(cat secrets/HippoSvcAcctDev.json)"
