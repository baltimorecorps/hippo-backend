#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

if [ "$#" -lt 1 ]; then
    echo "USAGE: $0 <skill_name>"
    exit 1
fi

source env/bin/activate
python ./get_skill_id.py $1
