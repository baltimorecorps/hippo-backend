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


if [ -z "$(docker images hippo_localdb -q)" ]; then
    echo "Building 'hippo_localdb' docker image..."
    docker build scripts/localdb -t hippo_localdb
    echo "Built 'hippo_localdb' docker image."
fi

if ! docker network ls | grep 'hippo-localdb'; then
    docker network create hippo-localdb
fi


if [ -z "$(docker ps -f name=hippo_localdb -q)" ]; then
    echo "Starting the 'hippo_localdb' docker container..."
    docker run \
        --name hippo_localdb \
        --network hippo-localdb \
        --rm -d \
        -p 5432:5432 \
        hippo_localdb
    echo "'hippo_localdb' container started."
fi

scripts/init_localdb.sh
