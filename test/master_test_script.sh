#!/bin/sh
# NB: We are executing this from inside /test/
set -e
cd ../src
echo "Starting test run: Nose"
nosetests ../test --with-gae --gae-lib-root=../google_appengine
echo "Test run complete: Nose"
echo "Starting test run: Jasmine"
jasmine-node --verbose --captureExceptions ../test/templatetest-spec.js
echo $?
echo "Test run complete: Jasmine"
echo "All tests complete."