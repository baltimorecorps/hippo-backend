#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

if [[ ! "$(python3 --version)" =~ Python.3\.[789].* ]]; then
    echo 'You must have Python 3.7 or later installed'
    exit 1
fi

if [ -d env ]; then
    echo 'Found environment, skipping virtual environment install.'
    . env/bin/activate
else
    echo "Setting up new virtual environment 'env'..."
    python3 -m venv env
    . env/bin/activate
    pip install -r requirements.txt
fi




