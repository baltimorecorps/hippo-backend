#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

docker run -it --rm --network hippo-localdb \
           -e PGPASSWORD=localdbpw postgres \
    psql -h hippo_localdb -U postgres localdb
