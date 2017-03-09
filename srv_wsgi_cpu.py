"""
    Return a JSON string converted from a large(ish) array of numbers.
"""

import json
import time
from misc.utils import TEST_ITERS

def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps({'message': [i for i in range(TEST_ITERS)] }).encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 5000, app)
    srv.serve_forever()
