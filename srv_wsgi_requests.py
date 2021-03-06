"""
    The endpoint makes a request to a remote site.
"""

import os, json, time
import requests
from misc.utils import TEST_URL

TEST_URL += str(int(time.time()))

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [requests.get(TEST_URL).text.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 5000, app)
    srv.serve_forever()
