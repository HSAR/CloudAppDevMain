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

number_of_queues = 10
edited_jingles_key = 'Edited Jingles'
taskHandlerRunning = False
noEditedJinglesCount = 0
start_lock = threading.Lock()

def makeSureTaskHandlerIsRunning():
    
    with start_lock:
        global taskHandlerRunning
        if not taskHandlerRunning:
            taskHandlerRunning = True
            taskqueue.add(url='/tasks/work')


class AutoHandler(webapp2.RequestHandler):
    def post(self):
        global noEditedJinglesCount
        global taskHandlerRunning
        logging.info("start task handler")
        client_jingles = memcache.Client()
        
        edited_jingles = client_jingles.get(edited_jingles_key)
        
        if edited_jingles == None:
            logging.info("cant find edited jingles, getting from data store")
            edited_jingles = datastore.getEditedJingles()
            client_jingles.add(edited_jingles_key, json.dumps(edited_jingles), 300)
        else:
            edited_jingles = json.loads(edited_jingles)
        
        if len(edited_jingles) > 0:
            logging.info("jingles are being edited")
            noEditedJinglesCount = 0
            key_list = []
            for jid in edited_jingles:
                logging.info("Edited Jingle has Id: " + jid)
                key_list.append(jid)
            
            client = memcache.Client()
            actions = client.get_multi(keys=key_list, for_cas=True)
            logging.info("prepare to see actions")
            logging.info(actions)
            actions_removed = {}
            for key in actions:
                logging.info("action key is: " + key)
                actions_removed[key] = json.dumps([])

            remaining_keys = client.cas_multi(mapping=actions_removed)
            logging.info("remaining keys: " + str(remaining_keys))
            
            while len(remaining_keys) > 0:
                logging.info("updating actions")
                newer_actions = client.get_multi(keys=remaining_keys, for_cas=True)
                actions_removed = {}
                for key, val in newer_actions.iteritems():
                    actions[key] = val
                    actions_removed[key] = json.dumps([])
                
                remaining_keys = client.cas_multi(mapping=actions_removed)
            
            actions_loaded = {}
            for key in actions:
                logging.info("loading key: " + key)
                actions_loaded[key] = json.loads(actions[key])
            
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
                
                logging.info("processing " + str(len(current_slice)) + " items")
                
                
                action_slice = {}
                for key in current_slice:
                    logging.info("key: " + key)
                    if key in actions_loaded and actions_loaded[key] != []:
                        logging.info("it has some actions")
                        action_slice[key] = {}
                        action_slice[key]["actions"] = actions_loaded[key]
                        action_slice[key]["tokens"] = edited_jingles[key]
                
                if len(action_slice) > 0:
                    logging.info("adding a task to a task queue")
                    queue_name = "TaskQueue" + str(current_queue)
                    payload = json.dumps(action_slice)
                    taskqueue.add(url = '/tasks/processjinglesactions',
                                    queue_name = queue_name,
                                    headers = {'Content-Type':'application/json'},
                                    payload = payload
                                    )
                
                current_queue += 1
        else:
            logging.info("no jingles are being edited")
            noEditedJinglesCount += 1
        
        
        if noEditedJinglesCount > 10:
            logging.info("stopping task handler")
            taskHandlerRunning = False
        else:
            taskqueue.add(url='/tasks/work')
        
        self.response.set_status(200)


class UpdateHandler(webapp2.RequestHandler):
    
    def post(self):
        action_dict_json = self.request.body
        action_dict = json.loads(action_dict_json)
        
        def update_jingle(jid, data_dict):
            
            @ndb.transactional
            def update_jingle_internal(jid, data_dict):
                
                jingle = datastore.getJingleJSON(jid)
                new_action_list = []
                
                for action in data_dict["actions"]:
                    
                    if action["action"] == "noteAdd":
                        jingle, new_action = jingle_update.add_note(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "noteRm":
                        jingle, new_action = jingle_update.remove_note(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "tempo":
                        jingle, new_action = jingle_update.change_tempo(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "subDivisions":
                        jingle, new_action = jingle_update.change_sub_divisions(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "instrumentAdd":
                        jingle, new_action = jingle_update.add_instrument(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "instrumentRm":
                        jingle, new_action = jingle_update.remove_instrument(jingle, action)
                        new_action_list.append(new_action)
                    
                    elif action["action"] == "instrumentEdit":
                        jingle, new_action = jingle_update.edit_instrument(jingle, action)
                        new_action_list.append(new_action)
                    
                    else:
                        print "Invalid"

                datastore.changeJingle(jid, jingle)
                
                for token in data_dict["tokens"]:
                    channel.send_message(token, json.dumps(new_action_list))
                
            while True:
                try:
                    update_jingle_internal(jid, data_dict)
                    break
                except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                    time.sleep(1)
            
            
        threads = []
        for jid, data_dict in action_dict.iteritems():
            work_thread = threading.Thread(target=update_jingle, kwargs={"jid":jid, "data_dict":data_dict})
            threads.append(work_thread)
            work_thread.start()
        
        for thread in threads:
            thread.join()
        
        self.response.set_status(200)



application = webapp2.WSGIApplication([
                    webapp2.Route(r'/tasks/work', handler=AutoHandler, name='auto-handler'),
                    webapp2.Route(r'/tasks/processjinglesactions', handler=UpdateHandler, name='update'),
                      ], debug=True)
