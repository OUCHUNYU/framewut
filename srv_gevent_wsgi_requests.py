"""
    This uses gevent and async requests to make a request to a second endpoint.
"""

from gevent import wsgi
from gevent import monkey
monkey.patch_all()
from requests_futures.sessions import FuturesSession

import json
import time

session = FuturesSession()

# NOTE should be the same for all servers testing the same thing...
TEST_URL = 'http://google.com/ishouldproducea404' 

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    fut = session.get(TEST_URL)
    resp = fut.result()
    return [resp.text.encode('utf-8')]

if __name__ == '__main__':
    wsgi.WSGIServer(
        ('0.0.0.0', 5000),
        app,
        log=None,
        spawn=10
    ).serve_forever()
