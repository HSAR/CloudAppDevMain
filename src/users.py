#!/usr/bin/env python

import os
import datetime

import webapp2
import jinja2

import json

import datastore
import error

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class UsernameHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if not username:
            return error.respond(400, "Missing request parameter(s)")
        else:
            result = datastore.getUserByUsername(username)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(db.to_dict(result)))
                self.response.set_status(200)
            return



class UserIDHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            result = datastore.getUserById(uid)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(db.to_dict(result)))
                self.response.set_status(200)
            return



class UserSongsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            result = datastore.getUsersSongs(uid)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(result))
                self.response.set_status(200)
            return


class UserCollabsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            result = datastore.getUserCollabs(uid)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(result))
                self.response.set_status(200)
            return


class UserInvitesHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            result = datastore.getCollabInvites(uid)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(result))
                self.response.set_status(200)
            return


application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/users', handler=UsernameHandler,
                                                        name='user-get-by-name'),
                                          webapp2.Route(r'/users/<uid>', handler=UserIDHandler,
                                                        name='user-get-by-id'),
                                          webapp2.Route(r'/users/<uid>/songs', handler=UserSongsHandler,
                                                        name='user-get-songs'),
                                          webapp2.Route(r'/users/<uid>/collabs', handler=UserCollabsHandler,
                                                        name='user-get-collabs'),
                                          webapp2.Route(r'/users/<uid>/invites', handler=UserInvitesHandler,
                                                        name='user-get-invites'),
                                      ], debug=True)
					
