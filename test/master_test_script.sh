# NB: We are executing this from inside /test/
cd ../src
nosetests ../test --with-gae --gae-lib-root=../google_appengine
jasmine-node --verbose ../test/templatetest-spec.js