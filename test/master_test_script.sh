#!/bin/sh
# NB: We are executing this from inside /test/
set -e
cd ../src
echo "Starting test run: Nose"
nosetests ../test --with-gae --gae-lib-root=../google_appengine
echo "Test run complete: Nose"
echo "----------------------------------------------------------------------"
echo "Setting up test run: Jasmine"
../google_appengine/dev_appserver.py ../src --skip_sdk_update_check &
sleep 1
echo "Starting test run: Jasmine"
jasmine-node --verbose --captureExceptions ../test/
echo "Test run complete: Jasmine"
echo "----------------------------------------------------------------------"
cd ..
echo "Starting test run : QUnit"
grunt --verbose --force
echo "All tests complete."