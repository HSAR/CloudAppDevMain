# NB: We are executing this from inside /test/
set -e
cd ../src
nosetests ../test --with-gae --gae-lib-root=../google_appengine
jasmine-node --verbose ../test/templatetest-spec.js