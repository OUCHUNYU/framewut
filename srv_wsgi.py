"""
To run for testing:

    ./misc/gunicorn_sync_srv.sh srv_wsgi
"""

import json
import os

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps({'message': 'helowrld'}).encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 5000, app)
    srv.serve_forever()
