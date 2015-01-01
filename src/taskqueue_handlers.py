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

#This is called when a user starts editing a song to ensure the "work" task
#queue is running. It needs to run in order to process the actions
def makeSureTaskHandlerIsRunning():
    
    with start_lock:
        global taskHandlerRunning
        if not taskHandlerRunning:
            taskHandlerRunning = True
            taskqueue.add(url='/tasks/work')


#This is request handler for the work task queue whose job is to split up the
#pending actions and give them to several processor task queues to deal with them
class AutoHandler(webapp2.RequestHandler):
    def post(self):
        global noEditedJinglesCount #used to determine when to stop calling work
        global taskHandlerRunning
        client_jingles = memcache.Client()
        
        #get the dictionary of currently edited jingles and the clients tokens
        edited_jingles = client_jingles.get(edited_jingles_key)
        
        if edited_jingles == None:
            #get from datastore if memcache empty and then add back to memcache
            edited_jingles = datastore.getEditedJingles()
            client_jingles.add(edited_jingles_key, json.dumps(edited_jingles), 300)
        else:
            edited_jingles = json.loads(edited_jingles)
        
        if len(edited_jingles) > 0:
            #if there are actually jingles edited
            noEditedJinglesCount = 0    #set back to 0
            #gets all the Jingle Ids from the dictionary
            key_list = []
            for jid in edited_jingles:
                key_list.append(jid)
            
            client = memcache.Client()
            #get all of the pending actions from the memcache for the currently
            #edited jingles. Each Jingle ID is a key in the memcache
            actions = client.get_multi(keys=key_list, for_cas=True)
            #we want to delete all the actions we are going to process from
            #the memcache.
            actions_removed = {}
            for key in actions:
                #set actions_removed to be a dictionary from JID to empty list
                actions_removed[key] = json.dumps([])

            #attempt to set all the memcahce keys at once
            #remaining keys contains a list of those which failed to be set
            #because their values have already changed again
            remaining_keys = client.cas_multi(mapping=actions_removed)
            
            #loop until we have managed to deal with all the remaining keys
            while len(remaining_keys) > 0:
                newer_actions = client.get_multi(keys=remaining_keys, for_cas=True)
                actions_removed = {}
                for key, val in newer_actions.iteritems():
                    #update our pending actions with the newer actions
                    actions[key] = val
                    actions_removed[key] = json.dumps([])
                
                remaining_keys = client.cas_multi(mapping=actions_removed)
            
            actions_loaded = {}
            for key in actions:
                #memcache stores the serialised action list so we need to 
                #deserialise them
                actions_loaded[key] = json.loads(actions[key])
            
            key_list.sort()
            
            #work out the number of jingles each task queue should process.
            #the minimum number is 5 to reduce the number of task queues needed
            #to keep overheads low and use less of the task queue quota
            jingles_per_queue = 5
            while (jingles_per_queue * number_of_queues) < len(key_list):
                jingles_per_queue += 1
            
            #actions are split into slices and each task queue deals with a 
            #slice. An action slice contains all the pending actions for
            #several jingles up to the number of jingles_per_queue. The slice
            #also contains a list of client tokens for each jingle
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
                    if key in actions_loaded and actions_loaded[key] != []:
                        action_slice[key] = {}
                        action_slice[key]["actions"] = actions_loaded[key]
                        action_slice[key]["tokens"] = edited_jingles[key]
                
                if len(action_slice) > 0:
                    #if this action_slice contains actions to be processed
                    #get the correct queue to process the jingle actions
                    queue_name = "TaskQueue" + str(current_queue)
                    payload = json.dumps(action_slice)
                    taskqueue.add(url = '/tasks/processjinglesactions',
                                    queue_name = queue_name,
                                    headers = {'Content-Type':'application/json'},
                                    payload = payload
                                    )
                
                current_queue += 1
        else:
            #increment if there are no jingles being edited
            noEditedJinglesCount += 1
        
        
        if noEditedJinglesCount > 10:
            #if no jingles have been edited 10 times in a row then we stop running
            #the work task queue
            taskHandlerRunning = False
        else:
            taskqueue.add(url='/tasks/work')
        
        self.response.set_status(200)


#This is the request handler for the task queues which actually process the 
#jingle actions
class UpdateHandler(webapp2.RequestHandler):
    
    def post(self):
        #all the action data is in the post payload
        action_dict_json = self.request.body
        action_dict = json.loads(action_dict_json)
        
        def update_jingle(jid, data_dict):
            
            @ndb.transactional
            def update_jingle_internal(jid, data_dict):
                #get the jingle json for this particular jingle
                jingle = datastore.getJingleJSON(jid)
                #the new action list will contain a copy of all the original 
                #actions but with the added checksum field to each one
                new_action_list = []
                #perform the correct action depending on action type
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

                #save the updated jingle
                datastore.changeJingle(jid, jingle)
                
                for token in data_dict["tokens"]:
                    #now send the list of processed actions to the clients
                    #working on the jingle
                    channel.send_message(token, json.dumps(new_action_list))
                
            while True:
                try:
                    update_jingle_internal(jid, data_dict)
                    break
                except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                    time.sleep(1)
            
            
        #first of all, each Jingle this task queue needs to deal with are divided
        #into individual threads for processing that individual jingles actions
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
