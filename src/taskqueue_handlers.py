import webapp2

import json
import threading

from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel

import memcache

import datastore

number_of_queues = 10

class AutoHandler(webapp2.RequestHandler):
    def post(self):
        client = memcache.Client()
        edited_jingles = JinglrMap.query(JinglrMap.is_being_edited == True).fetch()
        key_list = []
        for jm in edited_jingles:
            key_list.append(jm.jingle_id)

        actions = client.get_multi(key=key_list, for_cas=True)
        actions_removed = {}
        for key in actions:
            actions_removed[key] = []

        remaining_keys = client.cas_multi(mapping=actions_removed)

        while len(remaining_keys) > 0:
            newer_actions = client.get_multi(key=remaining_keys, for_cas=True)
            actions_removed = {}
            for key, val in newer_actions:
                actions[key] = val
                actions_removed[key] = []

            remaining_keys = client.cas_multi(mapping=actions_removed)

        key_list.sort()

        jingles_per_queue = 5
        while (jingles_per_queue * number_of_queues) < len(key_list):
            jingles_per_queue += 1

        start = 0
        end = jingles_per_queue
        items_processed = 0
        current_queue = 0
        while items_processed < len(key_list): 
            current_slice = key_list[start:end]
            start = end
            end += jingles_per_queue
            items_processed += len(current_slice)
            
            action_slice = {}
            for key in current_slice:
                action_slice[key] = actions[key]

            
            queue_name = "TaskQueue" + str(current_queue)
            payload = json.dumps(action_slice)
            taskqueue.add(url = '/tasks/processjinglesactions',
                            queue_name = queue_name,
                            headers = {'Content-Type':'application/json'},
                            payload = payload
                            )

class UpdateHandler(webapp2.RequestHandler):    

    def post(self):
        action_dict_json = self.request.body
        action_dict = json.loads(action_dict_json)

        def update_jingle(jid, action_list):
            
            @ndb.transactional(xg=True)
            def update_jingle_internal(jid, action_list):
                
                jingle = datastore.getJingleById(jid)
                jingle_json = jingle.jingle

                for action in action_list:
                
                    if action["action"] == "noteAdd":

                
                    elif action["action"] == "noteRm":


                    elif action["action"] == "tempo":


                    elif action["action"] == "subDivisions":


                    elif action["action"] == "instrumentAdd":


                    elif action["action"] == "instrumentRm":


                    elif action["action"] == "instrumentEdit":


                    else:
                        #Invalid

                jingle.jingle = jingle_json
                jingle.put()

                jm = ndb.Key('JinglrMap', jid + 'Map').get()
                if jm:
                    for 

            while True:
                try:
                    update_jingle_internal(jid, action_list)
                    break
                except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                    time.sleep(1)
                

        for jid, action_list_json in action_dict:
            action_list = json.loads(action_list_json)
            
            work_thread = threading.Thread(target=update_jingle, kwargs={"jid":jid, "action_list":action_list})
            work_thread.start()              


          

class RemoveNoteHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        @ndb.transactional(xg=True)
        def removeNote():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_track = action['track']
                action_noteid = action['noteId']
                
                track = jingle_json['tracks'][action_track]
                if len(track) != 0:
                    noteRemoved = False
                    for note in track['notes']:
                        if note['id'] == action_noteid:
                            track['notes'].remove(note)
                            noteRemoved = True
                            break
                    if noteRemoved:
                        jingle_json['tracks'][action_track] = track
                        jingle.jingle = jingle_json
                        jingle.put()
                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            removeNote()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)


class TempoHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def changeTempo():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_tempo = action['tempo']
                jingle_json['head']['tempo'] = action_tempo                    
                jingle.jingle = jingle_json
                jingle.put()
                                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            changeTempo()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)

class SubDivHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def changeSubDiv():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_subdiv = action['subDivisions']
                jingle_json['head']['subDivisions'] = action_subdiv                    
                jingle.jingle = jingle_json
                jingle.put()
                                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            changeSubDiv()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)


class AddInstrumentHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def addInstrument():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_tracknum = action['intrument']['track']
                action_instrument = action['instrument']['inst']
                jingle_tracks = jingle_json['tracks']

                if len(jingle_tracks[action_tracknum]) == 0:
                    
                    jingle.jingle = jingle_json
                    jingle.put()
                else:
                    
                                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            addInstrument()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)


class RemoveInstrumentHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def removeInstrument():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_tracknum = action['instrumentTrack']
                jingle_json['tracks'][action_tracknum] = {}                    
                jingle.jingle = jingle_json
                jingle.put()
                                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            removeInstrument()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)


class EditInstrumentHandler(webapp2.RequestHandler):
    def post(self):
        actionjson = self.request.body
        action = json.loads(actionjson)
        jid = action['jid']
        taskqueue = action['taskqueueName']
        
        
        
        @ndb.transactional(xg=True)
        def editInstrument():
            jingle = datastore.getJingleById(jid)
            if jingle:
                jingle_json = jingle.jingle
                action_tracknum = action['instrumentTrack']
                action_instrument = action['instrumentNumber']
                jingle_tracks = jingle_json['tracks']

                if len(jingle_tracks[action_tracknum]) != 0:
                    jingle_tracks[action_tracknum]['instrument'] = action_instrument
                    jingle_json['tracks'] = jingle_tracks
                    jingle.jingle = jingle_json
                    jingle.put()
                else:
                    #discard
                                
                jm = datastore.taskqueueWithName(taskqueue)
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, actionjson)
        
        try:
            editInstrument()
            self.response.set_status(200)
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            self.response.set_status(500)

                        
application = webapp2.WSGIApplication([
                    webapp2.Route(r'/tasks/startautoqueue', handler=AutoHandler, name='auto-start'),
                    webapp2.Route(r'/tasks/processjinglesactions', handler=UpdateHandler, name='update'),
                    webapp2.Route(r'/tasks/removenote', handler=RemoveNoteHandler, name='note-remove'),
                    webapp2.Route(r'/tasks/tempo', handler=TempoHandler, name='tempo'),
                    webapp2.Route(r'/tasks/subdiv', handler=SubDivHandler, name='subdiv'),
                    webapp2.Route(r'/tasks/addinstrument', handler=AddInstrumentHandler, name='instrument-add'),
                    webapp2.Route(r'/tasks/removeinstrument', handler=RemoveInstrumentHandler, name='instrument-remove'),
                    webapp2.Route(r'/tasks/editinstrument', handler=EditInstrumentHandler, name='instrument-edit'),
                      ], debug=True)
