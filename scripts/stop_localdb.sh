#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ -z "$(docker ps -f name=hippo_localdb -q)" ]; then
    echo "No current 'hippo_localdb' docker container running"
else
    echo "Stopping current 'hippo_localdb' docker container..."
    docker stop hippo_localdb
fi

