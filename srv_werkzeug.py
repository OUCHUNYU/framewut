"""
To run for testing:

    ./misc/gunicorn_sync_srv.sh srv_werkzeug

or
    ./misc/gunicorn_sync_srv.sh srv_werkzeug "meinheld.gmeinheld.MeinheldWorker"

to change out the worker.
"""

from werkzeug.wrappers import Request, Response
import json
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@Request.application
def app(request):
    return Response(
        json.dumps({'message': 'helowrld'}).encode('utf-8'),
        mimetype='application/json')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app)
