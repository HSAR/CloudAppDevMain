import webapp2

import json
import threading
import logging

from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel
from google.appengine.api import memcache
from google.appengine.api import taskqueue

import datastore
import jingle_update

from models import JinglrMap, Jingle

number_of_queues = 10

class StartAutoHandler(webapp2.RequestHandler):
    def get(self):
        taskqueue.add(url='/tasks/work')
    

class AutoHandler(webapp2.RequestHandler):
    def post(self):
        logging.info("first")
        client = memcache.Client()
        edited_jingles = JinglrMap.query(JinglrMap.is_being_edited == True).fetch()
        key_list = []
        for jm in edited_jingles:
            key_list.append(jm.jingle_id)

        actions = client.get_multi(keys=key_list, for_cas=True)
        actions_removed = {}
        for key in actions:
            print "removing an action"
            actions_removed[key] = json.dumps([])

        remaining_keys = client.cas_multi(mapping=actions_removed)

        while len(remaining_keys) > 0:
            newer_actions = client.get_multi(keys=remaining_keys, for_cas=True)
            actions_removed = {}
            for key, val in newer_actions.iteritems():
                actions[key] = val
                actions_removed[key] = json.dumps([])

            remaining_keys = client.cas_multi(mapping=actions_removed)
            
        actions_loaded = {}
        for key in actions:
            actions_loaded[key] = json.loads(actions[key])

        key_list.sort()
        
        print "just sorted"
        
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
            logging.info("Should always happen")
            for key in current_slice:
                if key in actions_loaded and actions_loaded[key] != []:
                    print actions[key]
                    action_slice[key] = actions_loaded[key]

            if len(action_slice) > 0:
                print "Running update"
                queue_name = "TaskQueue" + str(current_queue)
                payload = json.dumps(action_slice)
                taskqueue.add(url = '/tasks/processjinglesactions',
                                queue_name = queue_name,
                                headers = {'Content-Type':'application/json'},
                                payload = payload
                                )
                            
            current_queue += 1
            
            
        taskqueue.add(url='/tasks/work')

class UpdateHandler(webapp2.RequestHandler):    

    def post(self):
        action_dict_json = self.request.body
        action_dict = json.loads(action_dict_json)

        def update_jingle(jid, action_list):
            
            @ndb.transactional(xg=True)
            def update_jingle_internal(jid, action_list):
                
                jingle = datastore.getJingleById(jid)
                jingle_json = jingle.jingle
                new_action_list = []

                for action in action_list:
                
                    if action["action"] == "noteAdd":
                        print "Not here yet, fool!"
                
                    elif action["action"] == "noteRm":
                        jingle_json, new_action = jingle_update.remove_note(jingle_json, action)
                        new_action_list.append(new_action)

                    elif action["action"] == "tempo":
                        print "gone fishing"

                    elif action["action"] == "subDivisions":
                        print "overtime calls me"

                    elif action["action"] == "instrumentAdd":
                        print "be back soon honey"

                    elif action["action"] == "instrumentRm":
                        print "FAAAAAAAAAAK"

                    elif action["action"] == "instrumentEdit":
                        print "internet connection lost"

                    else:
                        print "Invalid"

                jingle.jingle = jingle_json
                jingle.put()

                jm = ndb.Key('JinglrMap', jid + 'Map').get()
                if jm:
                    for token in jm.editor_tokens:
                        channel.send_message(token, json.dumps(new_action_list))

            while True:
                try:
                    update_jingle_internal(jid, action_list)
                    break
                except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                    time.sleep(1)
                

        threads = []
        for jid, action_list in action_dict.iteritems():
            work_thread = threading.Thread(target=update_jingle, kwargs={"jid":jid, "action_list":action_list})
            threads.append(work_thread)
            work_thread.start()

        for thread in threads:
            thread.join()
        
        self.response.set_status(200)





                        
application = webapp2.WSGIApplication([
                    webapp2.Route(r'/tasks/work', handler=AutoHandler, name='auto-handler'),
                    webapp2.Route(r'/tasks/startautoqueue', handler=StartAutoHandler, name='auto-start'),
                    webapp2.Route(r'/tasks/processjinglesactions', handler=UpdateHandler, name='update'),
                    #webapp2.Route(r'/tasks/removenote', handler=RemoveNoteHandler, name='note-remove'),
                    #webapp2.Route(r'/tasks/tempo', handler=TempoHandler, name='tempo'),
                    #webapp2.Route(r'/tasks/subdiv', handler=SubDivHandler, name='subdiv'),
                    #webapp2.Route(r'/tasks/addinstrument', handler=AddInstrumentHandler, name='instrument-add'),
                    #webapp2.Route(r'/tasks/removeinstrument', handler=RemoveInstrumentHandler, name='instrument-remove'),
                    #webapp2.Route(r'/tasks/editinstrument', handler=EditInstrumentHandler, name='instrument-edit'),
                      ], debug=True)
