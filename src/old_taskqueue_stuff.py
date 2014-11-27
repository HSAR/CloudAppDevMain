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