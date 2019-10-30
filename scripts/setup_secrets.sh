#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

if [ -d secrets ]; then
    echo "Directory 'secrets' already exists. Skipping secrets setup."
    exit
else
    echo "Fetching secrets from Keybase..."
    git clone keybase://team/bcorps_hippo/secrets secrets
fi




