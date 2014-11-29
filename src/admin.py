#!/usr/bin/env python

import webapp2

import logging

import datastore

class Startup(webapp2.RequestHandler):
    def get(self):
        logging.info('======== Startup Running ========')
        logging.info('======== Startup Complete =======')


class ChannelDisconnect(webapp2.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        datastore.stopEditing(client_id)


application = webapp2.WSGIApplication([
                                        webapp2.Route(r'/_ah/warmup', handler=Startup, name='startup'),
                                        webapp2.Route(r'/_ah/channel/disconnected', handler=ChannelDisconnect, name='chan-disconnect'),
                                        ], debug=True)