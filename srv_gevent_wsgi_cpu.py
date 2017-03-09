"""
    Return a JSON string converted from a large(ish) array of numbers.
"""
from gevent import wsgi
from gevent import monkey
monkey.patch_all()

import json
from misc.utils import TEST_ITERS

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps({'message': [i for i in range(TEST_ITERS)]}).encode('utf-8')]

if __name__ == '__main__':
    srv = wsgi.WSGIServer(
        ('0.0.0.0', 5000),
        app,
        log=None,
        spawn=10
    )
    srv.serve_forever()
