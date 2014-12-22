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
import datetime

import webapp2
import jinja2

import json
import logging

from google.appengine import runtime
from google.appengine.api import users
from google.appengine.api import channel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    countTest = 0

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world!' + str(MainHandler.countTest))
        MainHandler.countTest += 1


class SearchPageHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'name': "Generic User",
        }
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        self.response.write(template.render(template_values))

class DashPageHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'name': "Generic User",
        }
        template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(template.render(template_values))


class TemplatePageHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'name': "Generic User",
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class JsonTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = {
            'test': 'success',
        }
        self.response.out.write(json.dumps(obj))


class JsonParameterTestHandler(webapp2.RequestHandler):
    def get(self, key):
        value = self.request.get('value')
        self.response.headers['Content-Type'] = 'application/json'
        obj = {
            key: value
        }
        self.response.out.write(json.dumps(obj))


class FiveHundredTestHandler(webapp2.RequestHandler):
    def get(self, key):
        raise runtime.DeadlineExceededError


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


application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/', handler=MainHandler, name='home'),
                                          webapp2.Route(r'/search', handler=SearchPageHandler, name='home'),
                                          webapp2.Route(r'/dashboard', handler=DashPageHandler, name='home'),
                                          webapp2.Route(r'/template', handler=TemplatePageHandler, name='template'),
                                          webapp2.Route(r'/test/json', handler=JsonTestHandler, name='jsonTest'),
                                          webapp2.Route(r'/test/json/<key:.*>', handler=JsonParameterTestHandler,
                                                        name='jsonParameterTest'),
                                          webapp2.Route(r'/fivehundred', handler=FiveHundredTestHandler,
                                                        name='fivehundred'),
                                      ], debug=True)
application.error_handlers[404] = Error404Handler
application.error_handlers[500] = Error500Handler
