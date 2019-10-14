#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d .git ]; then
    echo 'Please run this script from the root of your git repository'
    exit 1
fi

if ! docker --version; then
    echo 'You must have Docker installed to use the local database'
    exit 1
fi

if [ -z "$(docker ps -f name=hippo_localdb -q)" ]; then
    echo "'hippo_localdb container must be running to initalize it"
    exit 1
fi

run_db_cmd () {
    docker run -it --rm --network hippo-localdb \
               -e PGPASSWORD=localdbpw postgres \
           psql -h hippo_localdb -U postgres $@
}

if ! run_db_cmd localdb -c "SELECT 1" >/dev/null; then
    echo "Creating database localdb..."
    run_db_cmd -c "CREATE DATABASE localdb"
    source env/bin/activate
    python migrate.py db upgrade
    echo "Created database localdb."
else
    echo "Database localdb already found, skipping init"
fi
