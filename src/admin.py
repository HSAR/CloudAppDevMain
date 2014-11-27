#!/usr/bin/env python

import webapp2

import logging

import taskqueue

class Startup(webapp2.RequestHandler):
    def get(self):
        logging.info('======== Startup Running ========')
        logging.info('======== Startup Complete =======')

application = webapp2.WSGIApplication([
                                        webapp2.Route(r'/_ah/warmup', handler=Startup, name='startup'),
                                        ], debug=True)