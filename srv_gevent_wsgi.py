"""
    ./misc/gunicorn_sync_srv.sh srv_gevent_wsgi "meinheld.gmeinheld.MeinheldWorker"
"""
from gevent import wsgi
from gevent import monkey
monkey.patch_all()
import json

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps({'message': 'helowrld'}).encode('utf-8')]

if __name__ == '__main__':
    srv = wsgi.WSGIServer(
        ('0.0.0.0', 5000),
        app,
        log=None,
        spawn=10
    )
    srv.serve_forever()
