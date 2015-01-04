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

def test_search_name():
    createdata()
    response = app.get('/api/songs/search?query=Merry')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['jingle_id'] == '0'
    assert response.json['results'][0]['title'] == 'Merry Chistmas'
    assert response.json['results'][0]['genre'] == 'Snow Clouds'
    assert response.json['results'][0]['tags'] == ['Santa', 'Rudolf',
            'Tinsel, fool']

def test_search_tags():
    createdata()
    response = app.get('/api/songs/search?query=Rudolf')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert len(response.json['results']) == 1

def test_search_genre():
    createdata()
    response = app.get('/api/songs/search?query=Snow Clouds')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert len(response.json['results']) == 1

test_search_nonexistent.nosegae_datastore_v3 = True
test_search_nonexistent.nosegae_memcache = True
test_search_nonexistent.nosegae_channel = True
test_search_nonexistent.nosegae_taskqueue = True
test_search_name.nosegae_datastore_v3 = True
test_search_name.nosegae_memcache = True
test_search_name.nosegae_channel = True
test_search_name.nosegae_taskqueue = True
test_search_tags.nosegae_datastore_v3 = True
test_search_tags.nosegae_memcache = True
test_search_tags.nosegae_channel = True
test_search_tags.nosegae_taskqueue = True
test_search_genre.nosegae_datastore_v3 = True
test_search_genre.nosegae_memcache = True
test_search_genre.nosegae_channel = True
test_search_genre.nosegae_taskqueue = True
