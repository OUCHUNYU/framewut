"""
    The endpoint makes a request to another endpoint, but uses the async
    request_futures to do it.
"""

import json
import os
import requests

from requests_futures.sessions import FuturesSession
session = FuturesSession()

# NOTE should be the same for all servers testing the same thing...
TEST_URL = 'http://google.com/ishouldproducea404' 

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    fut = session.get(TEST_URL)
    resp = fut.result()
    return [resp.text.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 5000, app)
    srv.serve_forever()
