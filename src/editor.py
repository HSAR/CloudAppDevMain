#!/usr/bin/env python

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

class EditorPageHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			signout_bar = ('Signed in as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
			token = channel.create_channel(user.user_id())
			template_values = {
				'auth_bar': signout_bar,
				'token': token,
			}
			template = JINJA_ENVIRONMENT.get_template('templates/editor.html')
			self.response.write(template.render(template_values))
		
		else:
			self.abort(401)
		

		
application = webapp2.WSGIApplication([
					webapp2.Route(r'/editor/', handler=EditorPageHandler, name='editor'),
				      ], debug=True)