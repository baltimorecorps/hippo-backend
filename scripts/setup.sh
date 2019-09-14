#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

scripts/setup_virtualenv.sh
scripts/setup_secrets.sh
scripts/start_localdb.sh

echo -e 'Run this command to complete setup:\nsource env/bin/activate\n'
echo -e 'To connect to the dev database: export DEPLOY_ENV=dev\n'
echo -e 'To start the server: python run.py'
