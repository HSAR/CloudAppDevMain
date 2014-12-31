#!/usr/bin/env python

import os
import datetime
import operator
import copy

import datastore
from models import Jingle

import webapp2
import jinja2

import json

from google.appengine.api import users
from google.appengine.api import channel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

datetimejson = lambda obj: ( obj.isoformat()
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime)
        else None )

class SearchPageHandler(webapp2.RequestHandler):
    def get(self, query=None, sort=None):
        if not query and not sort:
            self.abort(400)
        if query:
            jingle = {"title": query, "author": query, "genre": query, "tags":
                    query}
            if sort:
                results, token, more = datastore.searchJingle(jingle, sort,
                        False)
            else:
                results, token, more = datastore.searchJingle(jingle, "title",
                        False)
        else:
            jingle = {}
            if sort:
                results, token, more = datastore.searchJingle(jingle, sort,
                        False)
            else:
                results, token, more = datastore.searchJingle(jingle, "title",
                        False)
        self.response.out.write(json.dumps(results, default=datetimejson))




application = webapp2.WSGIApplication([
					webapp2.Route(r'/songs/search', handler=SearchPageHandler, name='search'),
                                        webapp2.Route(r'/songs/search/<query>', handler=SearchPageHandler, name='search-query'),
                                        webapp2.Route(r'/songs/search/<query>/<sort>', handler=SearchPageHandler, name='search-query-sort'),
                                        webapp2.Route(r'/songs/search//<sort>', handler=SearchPageHandler, name='search-sort')
				      ], debug=True)
