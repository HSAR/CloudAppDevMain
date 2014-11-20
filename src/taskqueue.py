from google.appengine.ext import ndb
from google.appengine.ext import db
from models import JinglrMap

import time
import logging

taskqueueNameBase = "TaskQueue"

root_jinglrmap_key = ndb.Key('JinglrMapRoot', 'jinglrmaproot')

#Checks for the presence of each expected JinglrMap in the datastore, and generates it if it is not found
def initialiseJinglrMaps():
    
    for i in range(0,10):
        
        while True:
            try:
                name = taskqueueNameBase + str(i)
                key = ndb.Key('JinglrMap', name, parent=root_jinglrmap_key)

                jm = key.get()
                #if not found, the JinglrMap must be generated
                if not jm:
                
                    jm = JinglrMap(parent=root_jinglrmap_key, 
                            id=name,
                            taskqueue_name=name,
                            map_id=i)
                    
                    jm.put()
                    
                    logging.info('JinglrMap for taskqueue' + str(i) + ' created.')
                    
                time.sleep(1) #sleep to avoid trouble with the write limit
                break
            except (db.Timeout, db.InternalError) as exep:
                time.sleep(1)