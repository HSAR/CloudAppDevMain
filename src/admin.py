#!/usr/bin/env python

import webapp2

import logging

import datastore

import time

from models import JinglrUser, Jingle, JinglrMap

class Startup(webapp2.RequestHandler):
    def get(self):
        logging.info('======== Startup Running ========')
        logging.info('======== Startup Complete =======')


#this handler is called by the channel service when it detects a channel has
#been disconnected. It calls stopEditing in the datastore to remove the
#corresponding client token from the relevant JinglrMap
class ChannelDisconnect(webapp2.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        logging.info('client id is: ' + client_id)
        datastore.stopEditing(client_id)
        self.response.set_status(200)

#this can be called to populate the datastore with some initial data for testing
class InitialDataLoader(webapp2.RequestHandler):
    def get(self):
        user_key = datastore.root_user_key
        ju = JinglrUser(parent=user_key,
                        id='114163773958786510855',
                        user_id='114163773958786510855', 
                        username='jinglrtest',
                        tags=[],
                        collab_invites=[]
                       )
        ju.put()
        ja = JinglrUser(parent=user_key,
                        id='101004599599427966408',
                        user_id='101004599599427966408',
                        username='jinglradmin',
                        tags=[],
                        collab_invites=[]
                       )
        ja.put()
        
        jingle = Jingle(id='0', jingle_id='0', title='Merry Chistmas', author='114163773958786510855', genre='Snow Clouds', tags=['Santa', 'Rudolf', 'Tinsel, fool'])
        jingle_json = {}
        jingle_json['head'] = {'subDivisions':8, 'tempo':120, 'barLength':4}
        jingle_json['tracks'] = []
        for i in range(0,15):
            jingle_json['tracks'].append({})
        jingle.jingle = jingle_json
    
        jingle.collab_users = []
        
        jingle.put()
        
        jm = JinglrMap(id='0Map', jingle_id='0', client_ids = [])
        jm.put()           
            
        time.sleep(10)
        token = datastore.beginEditing('0')
        token = token['token']
        
        addInst = {
                      "action": "instrumentAdd",
                      "actionId": 'ho ho ho',
                      "instrument": {
                        "track": 0,
                        "inst": 0
                      }
                    }
        datastore.submitAction('0', addInst)
        tempo = {
          "action": "tempo",
          "actionId": "slow",
          "tempo": 60
        }
        datastore.submitAction('0', tempo)
        addNote = {
          "action": "noteAdd",
          "actionId": 'we',
          "note": {
            "id": 'a',
            "pos": 0,
            "track": 0,
            "pitch": 48,
            "length":4
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'wish',
          "note": {
            "id": 'b',
            "pos": 4,
            "track": 0,
            "pitch": 53,
            "length":2
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'you',
          "note": {
            "id": 'c',
            "pos": 6,
            "track": 0,
            "pitch": 53,
            "length":1
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'a',
          "note": {
            "id": 'd',
            "pos": 7,
            "track": 0,
            "pitch": 55,
            "length":1
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'mer',
          "note": {
            "id": 'e',
            "pos": 8,
            "track": 0,
            "pitch": 53,
            "length":1
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'ry',
          "note": {
            "id": 'f',
            "pos": 9,
            "track": 0,
            "pitch": 52,
            "length":1
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'christ',
          "note": {
            "id": 'g',
            "pos": 10,
            "track": 0,
            "pitch": 50,
            "length":2
          }
        }
        datastore.submitAction('0', addNote)
        
        addNote = {
          "action": "noteAdd",
          "actionId": 'mas',
          "note": {
            "id": 'h',
            "pos": 12,
            "track": 0,
            "pitch": 50,
            "length":2
          }
        }
        datastore.submitAction('0', addNote)
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Initial Data Loaded')
        
application = webapp2.WSGIApplication([
                                        webapp2.Route(r'/_ah/warmup', handler=Startup, name='startup'),
                                        webapp2.Route(r'/_ah/channel/disconnected/', handler=ChannelDisconnect, name='chan-disconnect'),
                                        webapp2.Route(r'/admin/initialdata', handler=InitialDataLoader, name='initial_data'),
                                        ], debug=True)