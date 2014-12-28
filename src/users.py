#!/usr/bin/env python

import os
import datetime

import webapp2
import jinja2

import json

import datastore
import error
import permission

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class UserRootHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if not username:
            return error.respond(400, "Missing request parameter(s)")
        else:
            result = datastore.getUserByUsername(username)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(datastore.getUserDict(result)))
                self.response.set_status(200)

    def put(self):
        user = users.get_current_user()
        if not user:
            return error.respond(401, "Not signed in")
        else:
            uid = user.user_id()
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('username' in parsed_request_json):
                    return error.respond(400, "Missing request parameter(s)")
                else:
                    result = datastore.createUser(uid, parsed_request_json['username'])
                    if 'errorMessage' in result:
                        return error.respond(500, result['errorMessage'])
                    else:
                        self.response.write(json.dumps(result))
                        self.response.set_status(200)
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class UserIdentifiedHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Not signed in")
                else:
                    uid = user.user_id()
            result = datastore.getUserById(uid)
            if not result:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(datastore.getUserDict(result)))
                self.response.set_status(200)
            return

    def patch(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "You are not authorised to edit this user")
                else:
                    uid = user.user_id()
            if not permission.can_edit_user(uid):
                return error.respond(401, "You are not authorised to edit this user")
            else:
                try:
                    parsed_request_json = json.loads(self.request.body)
                    if not ('username' in parsed_request_json or
                                    'bio' in parsed_request_json or
                                    'tags' in parsed_request_json):
                        return error.respond(400, 'Missing property in request JSON')
                    else:
                        success = True
                        if 'username' in parsed_request_json:
                            result = datastore.updateUsername(uid, parsed_request_json['username'])
                            if 'errorMessage' in result:
                                return error.respond(500, result['errorMessage'])
                        if 'bio' in parsed_request_json:
                            result = datastore.updateBio(uid, parsed_request_json['bio'])
                            success &= result
                        if 'tags' in parsed_request_json:
                            result = datastore.updateTags(uid, parsed_request_json['tags'])
                            success &= result
                        if not success:
                            return error.respond(500, "One or more failures encountered while executing field updates")
                        else:
                            self.response.write(json.dumps(result))
                            self.response.set_status(200)
                except ValueError:
                    return error.respond(400, 'Invalid JSON in request body')


class UserSongsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getUsersSongs(uid)
            if result is None:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class UserCollabsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getUserCollabs(uid)
            if result is None:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class SingleCollabHandler(webapp2.RequestHandler):
    def delete(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            if not permission.can_remove_collab(jid, uid):
                return error.respond(401, "You are not authorised to execute this action")
            else:
                result = datastore.removeCollab(uid, jid)
                if 'errorMessage' in result:
                    return error.respond(500, result['errorMessage'])
                else:
                    self.response.write(json.dumps(result))
                    self.response.set_status(200)


class UserInvitesHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getCollabInvites(uid)
            if result is None:
                self.response.set_status(404)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class SingleInviteHandler(webapp2.RequestHandler):
    def put(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        elif not permission.jingle_owner(jid):
            return error.respond(401, "You are not authorised to invite a collaborator to this jingle")
        else:
            username = datastore.getUsernameByUID(uid)
            result = datastore.addCollabInvite(username, jid)
            if 'errorMessage' in result:
                return error.respond(500, result['errorMessage'])
            else:
                self.response.write(json.dumps(result))
                self.response.set_status(200)

    def delete(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if (uid == 'self'):
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            if not permission.can_edit_user(uid):
                return error.respond(401, "You are not authorised to edit this user")
            else:
                response = self.request.get("response")
                if not response:
                    return error.respond(400, 'Missing property in request URI')
                elif (response == 'true'):
                    accept = True
                elif (response == 'false'):
                    accept = False
                else:
                    return error.respond(400, 'Invalid property in request URI')
                result = datastore.answerCollabInvite(uid, jid, accept)
                if 'errorMessage' in result:
                    return error.respond(500, result['errorMessage'])
                else:
                    self.response.write(json.dumps(result))
                    self.response.set_status(200)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/users', handler=UserRootHandler,
                                                        name='user-get-by-name'),
                                          webapp2.Route(r'/users/<uid>', handler=UserIdentifiedHandler,
                                                        name='user-get-by-id'),
                                          webapp2.Route(r'/users/<uid>/songs', handler=UserSongsHandler,
                                                        name='user-get-songs'),
                                          webapp2.Route(r'/users/<uid>/collabs/<jid>', handler=SingleCollabHandler,
                                                        name='user-single-collab'),
                                          webapp2.Route(r'/users/<uid>/collabs', handler=UserCollabsHandler,
                                                        name='user-get-collabs'),
                                          webapp2.Route(r'/users/<uid>/invites/<jid>', handler=SingleInviteHandler,
                                                        name='user-single-invite'),
                                          webapp2.Route(r'/users/<uid>/invites', handler=UserInvitesHandler,
                                                        name='user-get-invites'),
                                      ], debug=True)
					
