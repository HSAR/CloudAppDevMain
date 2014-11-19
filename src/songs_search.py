#!/usr/bin/env python

import os
import datetime
import operator
import copy

import webapp2
import jinja2

import json

from google.appengine.api import users
from google.appengine.api import channel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

test_elements = [ { "name": "UKIP Calypso", "tags": ["racist", "clowns"],
                    "genre": "Comedy", "author": "The Independents",
                    "rating": 100, "dateCreated": datetime.date(2014, 10, 20),
                    "id": 2},
                  { "name": "Gangnam Style", "tags": ["meme", "irritating"],
                    "genre": "K-Pop", "author": "The Pumping Lemmas",
                    "rating": 90, "dateCreated": datetime.date(2012, 07, 15),
                    "id": 1},
                  { "name": "Steve Jobs", "tags": ["meme", "irritating"],
                    "genre": "K-Pop", "author": "The Pumping Lemmas",
                    "rating": 90, "dateCreated": datetime.date(2012, 07, 15),
                    "id": 3},
                  { "name": "Super Mario Bros. Overworld", "tags": ["meme", "irritating"],
                    "genre": "K-Pop", "author": "The Pumping Lemmas",
                    "rating": 90, "dateCreated": datetime.date(2012, 07, 15),
                    "id": 4},
                  { "name": "Tim Cook", "tags": ["meme", "irritating"],
                    "genre": "K-Pop", "author": "The Pumping Lemmas",
                    "rating": 90, "dateCreated": datetime.date(2012, 07, 15),
                    "id": 5},
                  { "name": "Your Mum Is So Fat", "tags": ["meme", "irritating"],
                    "genre": "K-Pop", "author": "The Fat Mothers",
                    "rating": 90, "dateCreated": datetime.date(2012, 07, 15),
                    "id": 6},
                  { "name": "Zubion", "tags": ["ou", "est", "la", "gare"],
                    "genre": "French", "author": "The IT Crowd",
                    "rating": 20, "dateCreated": datetime.date(1958, 10, 04),
                    "id": 0} ]

# XXX This is temporary, should use a better method when song class is written
song_fields = [ "name", "tags", "genre", "author", "rating", "dateCreated" ]

datetimejson = lambda obj: ( obj.isoformat()
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime)
        else None )

class SearchPageHandler(webapp2.RequestHandler):
    def get(self, query=None, sort=None):
        if not query and not sort:
            self.abort(400)
        if sort:
            if not sort in song_fields:
                self.abort(400)
        # This stuff will be handled by the database; this is just temporary to
        # test the web stuff
        if query:
            results = filter(lambda item: query in item["name"]
                             or query in item["tags"] or query in item["genre"]
                             or query in item["author"], test_elements)
        else:
            results = copy.deepcopy(test_elements)
        if sort:
            results.sort(key=operator.itemgetter(sort))
        self.response.out.write(json.dumps(results, default=datetimejson))




application = webapp2.WSGIApplication([
					webapp2.Route(r'/songs/search', handler=SearchPageHandler, name='search'),
                                        webapp2.Route(r'/songs/search/<query>', handler=SearchPageHandler, name='search-query'),
                                        webapp2.Route(r'/songs/search/<query>/<sort>', handler=SearchPageHandler, name='search-query-sort'),
                                        webapp2.Route(r'/songs/search//<sort>', handler=SearchPageHandler, name='search-sort')
				      ], debug=True)
