#!/usr/bin/env python

import os
import datetime

import datastore

import webapp2
import jinja2
import logging

import json

from google.appengine.datastore.datastore_query import Cursor

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

datetimejson = lambda obj: ( obj.isoformat()
                             if isinstance(obj, datetime.date) or \
                                     isinstance(obj, datetime.datetime)
                             else None )


class SearchPageHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("query", default_value=None)
        sort = self.request.get("sort", default_value=None)
        token = self.request.get("token", default_value=None)
        tag = self.request.get("tag", default_value=None)
        if token:
            results, cursor, more = datastore.resumeSearch(Cursor(
                urlsafe=token))
        elif query:
            jingle = {"title": query, "author": query, "genre": query, "tags":
                query}
            if tag:
                jingle["tags"] = tag
            if sort:
                results, cursor, more = datastore.searchJingle(jingle, sort,
                                                              False)
            else:
                results, cursor, more = datastore.searchJingle(jingle, "title",
                                                              False)
        else:
            jingle = {}
            if tag:
                jingle["tags"] = tag
            if sort:
                results, cursor, more = datastore.searchJingle(jingle, sort,
                                                              False)
            else:
                results, cursor, more = datastore.searchJingle(jingle, "title",
                                                              False)
        response = {"results": results, "token": (cursor.urlsafe() if cursor
                                                  else None), "more": more}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response, default=datetimejson))


application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/api/songs/search', handler=SearchPageHandler, name='search'),
                                      ], debug=True)
