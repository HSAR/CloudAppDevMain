#!/usr/bin/env python
import logging

import os
import datetime

import webapp2
import jinja2

import json

import datastore
import error
import permission

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ApiUserHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if not username:
            result = datastore.getAllUsers()
            if result:
                result = datastore.getUserList(result, False)
                self.response.write(json.dumps(result))
            self.response.set_status(200)
        else:
            result = datastore.getUserByUsername(username)
            if not result:
                return error.respond(404, "No user found for username " + username)
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
                        self.response.set_status(200)
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')

class ApiUserAutocompleteHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        results = datastore.completeUsername(username)
        self.response.write(json.dumps(results))
        self.response.set_status(200)

class ApiUserUidHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Not signed in")
                else:
                    uid = user.user_id()
                    result = datastore.getUserById(uid)
                    if not result:
                        create_user_result = datastore.createUser(uid, user.nickname())
                        if 'errorMessage' in create_user_result:
                            return error.respond(500, result['errorMessage'])
            result = datastore.getUserById(uid)
            if not result:
                return error.respond(404, "No user found for UID " + uid)
            else:
                self.response.write(json.dumps(datastore.getUserDict(result)))
                self.response.set_status(200)
            return

    def patch(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
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
                        result = datastore.updateUser(uid, parsed_request_json)
                        if 'errorMessage' in result:
                            return error.respond(500, result['errorMessage'])
                        else:
                            self.response.set_status(200)
                except ValueError:
                    return error.respond(400, 'Invalid JSON in request body')


class WebUserProfileHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Not signed in")
                else:
                    uid = user.user_id()
                    return self.redirect("/web/users/" + uid)
            template_values = {
                'uid': uid,
            }
            template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
            self.response.write(template.render(template_values))


class ApiUserUidSongsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getUsersSongs(uid)
            if result is None:
                return error.respond(404, "No user found for UID " + uid)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class ApiUserUidCollabsHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getUserCollabs(uid)
            if result is None:
                return error.respond(404, "No user found for UID " + uid)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class ApiUserUidCollabsUidHandler(webapp2.RequestHandler):
    def delete(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
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
                    self.response.set_status(200)


class ApiUserUidInvitesHandler(webapp2.RequestHandler):
    def get(self, uid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "Invalid user ID in request URL")
                else:
                    uid = user.user_id()
            result = datastore.getCollabInvites(uid)
            if result is None:
                return error.respond(404, "No user found for UID " + uid)
            else:
                self.response.write(json.dumps(datastore.getJingleList(result)))
                self.response.set_status(200)
            return


class ApiUserUidInvitesSidHandler(webapp2.RequestHandler):
    def put(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        elif not permission.jingle_owner(jid):
            return error.respond(401, "You are not authorised to invite a collaborator to this jingle")
        else:
            result = datastore.addCollabInvite(uid, jid)
            if 'errorMessage' in result:
                return error.respond(500, result['errorMessage'])
            else:
                self.response.set_status(200)

    def delete(self, uid, jid):
        if not uid:
            return error.respond(400, "Invalid user ID in request URL")
        else:
            if uid == 'self':
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
                elif response == 'true':
                    accept = True
                elif response == 'false':
                    accept = False
                else:
                    return error.respond(400, 'Invalid property in request URI')
                result = datastore.answerCollabInvite(uid, jid, accept)
                if 'errorMessage' in result:
                    return error.respond(500, result['errorMessage'])
                else:
                    self.response.set_status(200)


def Error404Handler(request, response, exception):
    logging.exception(exception)
    template_values = {
    }
    template = JINJA_ENVIRONMENT.get_template('templates/404.html')
    response.write(template.render(template_values))
    response.set_status(404)


def Error500Handler(request, response, exception):
    logging.exception(exception)
    template_values = {
    }
    template = JINJA_ENVIRONMENT.get_template('templates/500.html')
    response.write(template.render(template_values))
    response.set_status(500)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/api/users', handler=ApiUserHandler,
                                                        name='user-get-by-name'),
                                          webapp2.Route(r'/api/users/complete', handler=ApiUserAutocompleteHandler,
                                                        name='user-autocomplete'),
                                          webapp2.Route(r'/api/users/<uid>', handler=ApiUserUidHandler,
                                                        name='user-get-by-id'),
                                          webapp2.Route(r'/web/users/<uid>', handler=WebUserProfileHandler,
                                                        name='user-get-by-id'),
                                          webapp2.Route(r'/api/users/<uid>/songs', handler=ApiUserUidSongsHandler,
                                                        name='user-get-songs'),
                                          webapp2.Route(r'/api/users/<uid>/collabs/<jid>', handler=ApiUserUidCollabsUidHandler,
                                                        name='user-single-collab'),
                                          webapp2.Route(r'/api/users/<uid>/collabs', handler=ApiUserUidCollabsHandler,
                                                        name='user-get-collabs'),
                                          webapp2.Route(r'/api/users/<uid>/invites/<jid>', handler=ApiUserUidInvitesSidHandler,
                                                        name='user-single-invite'),
                                          webapp2.Route(r'/api/users/<uid>/invites', handler=ApiUserUidInvitesHandler,
                                                        name='user-get-invites'),
                                      ], debug=True)
application.error_handlers[404] = Error404Handler
application.error_handlers[500] = Error500Handler
					
