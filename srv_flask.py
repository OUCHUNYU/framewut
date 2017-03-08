"""
To run for testing:

    ./misc/gunicorn_sync_srv.sh srv_flask

or

    ./misc/gunicorn_sync_srv.sh srv_flask "meinheld.gmeinheld.MeinheldWorker"

to change out the worker.
"""
from flask import Flask
import json

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return json.dumps({'message': 'helowrld'}).encode('utf-8')

if __name__ == '__main__':
    app.run()
