"""
    Monkey-patched gevent implementation of a WSGI endpoint that demos behavior
    of a small sleep on the endpoint. The monkey patch is important here
    because a standard Python time.sleep() would block the main thread and
    hence the usefulness of gevent here.
"""

from gevent import wsgi
from gevent import monkey
monkey.patch_all()
import json, time


def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    time.sleep(0.1)
    return [json.dumps({'message': 'helowrld'}).encode('utf-8')]

if __name__ == '__main__':
    srv = wsgi.WSGIServer(
        ('0.0.0.0', 5000),
        app,
        log=None,
        spawn=10
    )
    srv.serve_forever()
