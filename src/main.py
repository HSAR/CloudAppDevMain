#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import webapp2
import jinja2

import json
import logging

import error

from google.appengine import runtime
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render())


class SearchPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        self.response.write(template.render())

class DashPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(template.render())


class UserHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_id = user.user_id()
            success_object = {
                'uid': user_id,
            }
            self.response.write(json.dumps(success_object))
            self.response.set_status(200)
        else:
            return error.respond(401, "You are not signed in")


def Error404Handler(request, response, exception):
    logging.exception(exception)
    template = JINJA_ENVIRONMENT.get_template('templates/404.html')
    response.write(template.render())
    response.set_status(404)


def Error500Handler(request, response, exception):
    logging.exception(exception)
    template = JINJA_ENVIRONMENT.get_template('templates/500.html')
    response.write(template.render())
    response.set_status(500)

class FiveHundredTestHandler(webapp2.RequestHandler):
    def get(self, key):
        raise runtime.DeadlineExceededError

application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/', handler=MainHandler, name='home'),
                                          webapp2.Route(r'/api/uid', handler=UserHandler, name='uid'),
                                          webapp2.Route(r'/search', handler=SearchPageHandler, name='search'),
                                          webapp2.Route(r'/dashboard', handler=DashPageHandler, name='dashboard'),
                                          webapp2.Route(r'/fivehundred', handler=FiveHundredTestHandler,
                                                        name='fivehundred'),
                                      ], debug=True)
application.error_handlers[404] = Error404Handler
application.error_handlers[500] = Error500Handler
