set -e
pwd
cd ../src
nosetests ../test --with-gae --gae-lib-root=../google_appengine