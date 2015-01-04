#!/usr/bin/env python2
import webtest
import songs_search
import admin
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

app = webtest.TestApp(songs_search.application)

def createdata():
    adminApp = webtest.TestApp(admin.application)
    response = adminApp.get('/admin/initialdata')
    assert response.status == '200 OK'

# Test search for nonexistent string
def test_search_nonexistent():
    createdata()
    response = app.get('/api/songs/search?query=DEADBEEF')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert len(response.json['results']) == 0

test_search_nonexistent.nosegae_datastore_v3 = True
test_search_nonexistent.nosegae_memcache = True
test_search_nonexistent.nosegae_channel = True
test_search_nonexistent.nosegae_taskqueue = True
