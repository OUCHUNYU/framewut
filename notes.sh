#!/usr/bin/env bash

function div {
    printf '=%.0s' {1..80}; echo
    printf "$1\n"
    printf '=%.0s' {1..80}; echo
}

rm -f /tmp/framewut_notes.log
touch /tmp/framewut_notes.log

function basic_test {
    div "$1 ($3)"
    ./misc/gunicorn_srv.sh $2 $3 2>>/tmp/framewut_notes.log &
    sleep 3 # let server startup
    resp=`curl http://0.0.0.0:5000`
    resp=`echo $resp| tr -d '\n' | tr -d ' '`
    echo "Fetching ${resp:0:50} ..."; echo
    ./misc/test_wrk.sh; echo; echo
    sleep 2
    ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill
}

### tests start
date

printf "
The following tests demonstrate the behavior of a simple 'hello world'
application that converts and returns a small JSON string. This is the most
basic of tests, designed to highlight the different characteristics of the
underlying frameworks.\n
"

basic_test "helowrld: vanilla wsgi" \
    srv_wsgi sync

basic_test "helowrld: vanilla wsgi" \
    srv_wsgi "meinheld.gmeinheld.MeinheldWorker"

basic_test "helowrld: werkzeug" \
    srv_werkzeug "meinheld.gmeinheld.MeinheldWorker"

basic_test "helowrld: flask" \
    srv_werkzeug "meinheld.gmeinheld.MeinheldWorker"

basic_test "helowrld: gevent/wsgi" \
    srv_gevent_wsgi gevent

basic_test "helowrld: gevent/wsgi" \
    srv_gevent_wsgi "meinheld.gmeinheld.MeinheldWorker"



printf "
These tests add a tiny sleep to the response. This is where gevent, with
async I/O (and a monkey patched time.sleep!) makes it's first hint of
difference.\n
"

basic_test "vanilla wsgi with sleep" \
    srv_wsgi_sleep sync

basic_test "vanilla wsgi with sleep" \
    srv_wsgi_sleep "meinheld.gmeinheld.MeinheldWorker"

basic_test "gevent with sleep" \
    srv_gevent_wsgi_sleep gevent 

basic_test "gevent with sleep" \
    srv_gevent_wsgi_sleep "meinheld.gmeinheld.MeinheldWorker"




printf "
For these tests the endpoint makes an HTTP request to a separate server.\n
"

basic_test "vanilla wsgi with requests" \
    srv_wsgi_requests sync
sleep 2
basic_test "vanilla wsgi with requests" \
    srv_wsgi_requests "meinheld.gmeinheld.MeinheldWorker"
sleep 4
basic_test "gevent with requests" \
    srv_gevent_wsgi_requests gevent
sleep 2
basic_test "gevent with async requests" \
    srv_gevent_wsgi_requests_futures gevent
sleep 2
basic_test "vanilla wsgi with async requests" \
    srv_wsgi_requests_futures sync
sleep 2
basic_test "vanilla wsgi with async requests" \
    srv_wsgi_requests_futures "meinheld.gmeinheld.MeinheldWorker"



printf "
These tests perform a relatively intensive CPU task (generating an array of numbers).\n
"

basic_test "CPU intensive: vanilla wsgi" \
    srv_wsgi_cpu sync

basic_test "CPU intensive: vanilla wsgi" \
    srv_wsgi_cpu "meinheld.gmeinheld.MeinheldWorker"

basic_test "CPU intensive: gevent/wsgi" \
    srv_gevent_wsgi_cpu gevent
