#!/usr/bin/env bash

lua_script="`dirname $0`/report_json.lua"

url="http://0.0.0.0:5000/"
wrk -d20s -t10 -c200 $url #-s $lua_script
