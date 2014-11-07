#!/usr/bin/env python

import webapp2

import json
import logging

from google.appengine.api import users
from google.appengine.api import channel

class GetToken(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        if user:
            token = channel.create_channel(user.user_id())
            obj = {
                'token': token,
            }
            self.response.out.write(json.dumps(obj))
        else:
            self.error(401)

application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/auth/token', handler=GetToken, name='token'),
                                      ], debug=True)