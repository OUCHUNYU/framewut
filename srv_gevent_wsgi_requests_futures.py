"""
    This uses gevent and async requests to hit a remote endpoint.
"""

import json, time
import requests

from gevent import wsgi
from gevent import monkey
monkey.patch_all()

from requests_futures.sessions import FuturesSession
from misc.utils import TEST_URL

TEST_URL += str(int(time.time()))

session = FuturesSession()

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
