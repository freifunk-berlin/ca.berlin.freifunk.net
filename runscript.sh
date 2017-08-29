#!/bin/bash

# Runs python script within virtualenv
# used by cron
# taken from http://scottbarnham.com/blog/2013/04/09/run-python-script-in-virtualenv-from-cron/index.html

cd `dirname $0`
source env/bin/activate
python "${@:1}"
