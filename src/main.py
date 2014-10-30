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

from google.appengine.api import users
from google.appengine.api import channel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world!')


class TemplatePageHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'name': "Generic User",
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class EditorPageHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			auth_html = ('Signed in as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
		else:
			auth_html = ('<a href="%s">Sign in or register</a>.' % users.create_login_url(self.request.uri))
		token = channel.create_channel(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
		template_values = {
			'auth_bar': auth_html,
			'token': token,
		}
		template = JINJA_ENVIRONMENT.get_template('templates/editor.html')
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


application = webapp2.WSGIApplication([
                                          ('/', MainHandler),
                                          ('/template', TemplatePageHandler),
                                          ('/editor', EditorPageHandler),
                                          ('/test/json', JsonTestHandler),
                                          ('/test/json/(.*)', JsonParameterTestHandler)
                                      ], debug=True)
