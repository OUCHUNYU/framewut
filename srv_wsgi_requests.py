"""
    Make a requests
"""

import json
import os
import requests

# NOTE should be the same for all servers testing the same thing... TODO should
# probably be in a shared lib
TEST_URL = 'http://google.com/ishouldproducea404' 

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [requests.get(TEST_URL).text.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 5000, app)
    srv.serve_forever()
