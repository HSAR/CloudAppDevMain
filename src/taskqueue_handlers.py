import webapp2

import json

from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel

import datastore

class RemoveNoteHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def removenote():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_track = action['track']
                action_noteid = action['noteId']
                
                track = jingle_json['tracks'][action_track]
                for note in track['notes']:
                    if note['id'] == action_noteid:
                        track['notes'].remove(note)
                        break
                jingle_json['tracks'][action_track] = track
                jingle.jingle = jingle_json
                jingle.put()
                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            removenote()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)
                        
                        
application = webapp2.WSGIApplication([
                    webapp2.Route(r'/tasks/removenote', handler=RemoveNoteHandler, name='note-remove'),
                      ], debug=True)