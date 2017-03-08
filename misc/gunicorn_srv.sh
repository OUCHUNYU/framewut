#!/usr/bin/env bash

if [ -z $1 ]; then
    echo "Usage: $0 \$server:app"
    echo " E.g.: $0 srv_wsgi:app        # where srv_wsgi corresponds to srv_wsgi.py"
    exit 1
fi
serve="$1:app"

if [ -z $2 ]; then              # "sync" is default
    echo "Serving $serve... with 'sync' worker"
    gunicorn $serve \
        --workers=10 \
        --bind=0.0.0.0:5000
else
    echo "Serving $serve... with '$2' worker"
    gunicorn $serve \
        --workers=10 \
        --bind=0.0.0.0:5000 \
        --worker-class="$2"     # e.g. "meinheld.gmeinheld.MeinheldWorker"
fi
