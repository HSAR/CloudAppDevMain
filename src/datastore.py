from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import taskqueue
from google.appengine.api import memcache

import datetime
import time
import random
import json
from google.appengine.api import channel
from models import JinglrUser, Jingle, JinglrMap

class Orderings:
    Title, Date, Rating, Length = range(4)
        
#we have two entity groups. Root keys are used to define the groups
#the first group is the group of users
root_user_key = ndb.Key('UserRoot', 'userroot')
#the second group is the group of jinglr maps
root_jinglrmap_key = ndb.Key('JinglrMapRoot', 'jinglrmaproot')
#MORE GOD DAMN GAE
dumb_value = "!62DJkTpFqQ#faV3qDa6Fk=K%MdqFMM=kpdrcRKT" # it's pretty dumb

#~~~~~~~~~~~~~~~~~~~~~~~~~ INTERNAL FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_jingle_id(uid):
    
    timestamp = datetime.datetime.now()
    rand = random.random()
    return uid + str(rand) + str(timestamp)


#Get the name of the task queue allocated to the jingle, or None if there isn't one
def getTaskqueueNameForJingle(jid):
    
    map_query = JinglrMap.query(JinglrMap.jingle_id==jid)
    jm = map_query.fetch()
    if jm:
        return jm[0].taskqueue_name
    else:
        return None


def getTaskqueueWithName(name):
    
    key = ndb.Key('JinglrMap', name, parent=root_jinglrmap_key)
    
    jm = key.get()
    if jm:
        return jm
    else:
        return None


def getUsernameByUID(uid):
    
    username = memcache.get(uid)
    if username is not None:
        return username
    else:
        user = getUserById(uid)
        if user is not None:
            username = user.username
            memcache.add(uid, username, 3600)
            return username
        else:
            return None


#~~~~~~~~~~~~~~~~~~~~~~~~~ READ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#takes a user id and returns the JingleUser Entity if one is found, or None
def getUserById(uid):
    
    user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
    user = user_key.get()
    if user:
        if dumb_value in user.tags:
            user.tags.remove(dumb_value)
        if dumb_value in user.collab_invites
        user.collab_invites.remove(dumb_value)
        return user
    else:
        return None


#takes a username and returns the JingleUser Entity if one is found, or None
def getUserByUsername(username):
    
    user_query = JinglrUser.query(ancestor=root_user_key).filter(JinglrUser.username == username)
    user_list = user_query.fetch()
    if user_list:
        user = user_list[0]
        if dumb_value in user.tags:
            user.tags.remove(dumb_value)
        if dumb_value in user.collab_invites
        user.collab_invites.remove(dumb_value)
        return user
    else:
        return None


#takes a user id and returns the list of jingles (possibly empty) that they created
def getUsersSongs(uid):
    
    jingle_query = Jingle.query(Jingle.author == uid)
    jingle_list = jingle_query.fetch(projection=[Jingle.jingle_id,
                                                 Jingle.title,
                                                 Jingle.date_created,
                                                 Jingle.genre,
                                                 Jingle.length,
                                                 Jingle.tags,
                                                 Jingle.collab_users])
    for jingle in jingle_list:
        if dumb_value in jingle.tags:
            jingle.tags.remove(dumb_value)
        if dumb_value in jingle.collab_users:
            jingle.collab_users.remove(dumb_value)
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
        
    return jingle_list


#takes a user id and returns the list of jingles (possibly empty) that the user is collaborating on
def getUserCollabs(uid):
    
    jingle_query = Jingle.query(Jingle.collab_users == uid)
    jingle_list = jingle_query.fetch(projection=[Jingle.jingle_id,
                                                 Jingle.title,
                                                 Jingle.author,
                                                 Jingle.date_created,
                                                 Jingle.genre,
                                                 Jingle.length,
                                                 Jingle.tags,
                                                 Jingle.collab_users])
    for jing in jingle_list:
        jing.username = getUsernameByUID(jing.author)
        
    for jingle in jingle_list:
        if dumb_value in jingle.tags:
            jingle.tags.remove(dumb_value)
        if dumb_value in jingle.collab_users:
            jingle.collab_users.remove(dumb_value)
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
    
    return jingle_list


#takes a user id and returns a list of jingles (possibly empty) that they have been invited to collaborate on
def getCollabInvites(uid):
    
    user = getUserById(uid)
    if user:
        invite_list = user.collab_invites
        jingle_list = []
        for jid in invite_list:
            current_jingle = getJingleById(jid, False)
            current_jingle.username = getUsernameByUID(current_jingle.author)
            jingle_list.append(current_jingle)
            
        for jingle in jingle_list:
            if dumb_value in jingle.tags:
                jingle.tags.remove(dumb_value)
            if dumb_value in jingle.collab_users:
                jingle.collab_users.remove(dumb_value)
            username_list = []
            for user_id in jingle.collab_users:
                username_list.append(getUsernameByUID(user_id))
            jingle.collab_usernames = username_list
        
        return jingle_list


#returns jingle entity it it exists, or None
def getJingleById(jingle_id, json=True):
    
    jingle = None
    if json:
        jingle_key = ndb.Key('Jingle', jingle_id)
        jingle = jingle_key.get()
    else:
        jingle_query = Jingle.query(Jingle.jingle_id == jingle_id)
        jingle_list = jingle_query.fetch(projection=[Jingle.jingle_id,
                                                     Jingle.title,
                                                     Jingle.author,
                                                     Jingle.date_created,
                                                     Jingle.genre,
                                                     Jingle.length,
                                                     Jingle.tags,
                                                     Jingle.collab_users])
        if jingle_list:
            jingle = jingle_list[0]
            
    if jingle:
        jingle.username = getUsernameByUID(jingle.author)
        
        if dumb_value in jingle.tags:
            jingle.tags.remove(dumb_value)
        if dumb_value in jingle.collab_users:
            jingle.collab_users.remove(dumb_value)
        
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
        
        return jingle
    else:
        return None


#~~~~~~~~~~~~~~~~~~~~~~~~~ BLOCKING WRITE FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~
#takes a uid and a username
#returns a dictionary.
#if there was an error:
    #{"error" : errorMessage}
#if successful:
    #{"userKey" : userKey}
def createUser(uid, username):
    
    @ndb.transactional
    def createUserInternal():
        
        existingUser = getUserById(uid)
        
        if existingUser:
            return {"errorMessage":"You have already registered an account"}
            
            
        existingUser = getUserByUsername(username)
        
        if existingUser:
            return {"errorMessage":"That username has already been taken"}
            
        
        ju = JinglrUser(parent=root_user_key, 
                        id=uid, 
                        user_id=uid, 
                        username=username,
                        tags=[dumb_value],
                        collab_invites=[dumb_value]
                       )
        
        result = ju.put()
        return {"userKey":result}
    
    
    if not username:
        return {"errorMessage":"Please enter a username"}
    
    result = None
    
    while True:
        try:
            result = createUserInternal()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)
    
    return result


#takes a user ID and a new username
#returns a dictionary in the form:
#   {"userKey" : userkey}
#when successful or:
#   {"errorMessage" : errorMessage}
#on a fail          
def updateUsername(uid, username):
    
    if not username:
        return {"errorMessage":"Please enter a username"}
    
    
    @ndb.transactional
    def updateUsernameInternal():
        
        existingUser = getUserByUsername(username)
        
        if existingUser:
            return {"errorMessage" : "That username has already been taken"}
            
        user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
        user = user_key.get()
        
        if not user:
            return {"errorMessage" : "That is not a valid user"}
        
        user.username = username
        result = user.put()
        return {"userKey" : result}
    
    
    result = None
    
    while True:
        try:
            result = updateUsernameInternal()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)
    
    return result


#takes a user id and a new bio. Returns the user entity key on success or None
#if that user does not exist
def updateBio(uid, bio):
    
    while True:
        try:
            user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
            user = user_key.get()
            if not user:
                return None
                
            user.bio = bio
            return user.put()
        except (db.Timeout, db.InternalError) as exep:
            time.sleep(1)


#takes a user ID and a new list of tags. Returns the user entity key on success
#or None if that user does not exist
def updateTags(uid, tags):
    
    tags.append(dumb_value)
    while True:
        try:
            user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
            user = user_key.get()
            if not user:
                return None
                
            user.tags = tags
            return user.put()
        except (db.Timeout, db.InternalError) as exep:
            time.sleep(1)


#takes stuff to create a jingle entity
#returns new jingle entity key once successful
def createJingle(uid, title, genre=None, tags=None):
    
    gen_id = generate_jingle_id(uid)
    
    jingle = Jingle(id=gen_id, jingle_id=gen_id, title=title, author=uid)
    if genre:
        jingle.genre = genre
    if tags:
        tags.append(dumb_value)
        jingle.tags = tags
    else:
        jingle.tags = [dumb_value]
    
    jingle_json = {}
    jingle_json['head'] = {'subDivisions':4, 'tempo':120}
    jingle_json['tracks'] = []
    jingle.jingle = jingle_json
    
    jingle.collab_users = [dumb_value]
    
    result = None
    while True:
        try:
            result = jingle.put()
            break
        except (db.Timeout, db.InternalError) as exep:
            time.sleep(1)
    
    return result


#called when a client wants to start editing a jingle
#in a success case it will return:
#   {"token" : channelToken}
#in a fail (because there are no free task queues) it will return:
#   {"errorMessage" : errorMessage}
def beginEditing(uid, jid):
    
    #first need to see if we are likely able to edit the jingle
    #is there already a JinglrMap in use for this Jingle?
    jm = JinglrMap.query(JinglrMap.jingle_id == jid).fetch()
    if not jm:
        #well, maybe there is a free one we can use?
        jm = JinglrMap.query(JinglrMap.jingle_id == None).fetch()
        if not jm:
            #no JinglrMap available, give up :(
            return {"errorMessage" : "Service currently busy. No available task queues"}
            
    #we think there is a JinglrMap free. Lets make a token of good faith
    channelToken = channel.create_channel(uid)
    
    @ndb.transactional
    def registerEditor():
        
        jm = JinglrMap.query(ancestor=root_jinglrmap_key).filter(JinglrMap.jingle_id == jid).fetch()
        if jm:
            #this is the JinglrMap already being used for this Jingle
            #update it with the new channelToken for the new editor user
            jingMap = jm[0]
            jingMap.editor_tokens.append(channelToken)
            jingMap.put()
            return True
        else:
            jm = JinglrMap.query(ancestor=root_jinglrmap_key).filter(JinglrMap.jingle_id == None).fetch()
            if jm:
                #we have a list of unused JinglrMap entities
                #select the first one to start with
                jingMap = jm[0]
                for map in jm:
                    #loop through all maps and select the one with the lowest map_id
                    if map.map_id < jingMap.map_id:
                        jingMap = map
                
                #jingMap is now set to the map we want to use
                jingMap.jingle_id = jid #first set it to be for this Jingle
                jingMap.editor_tokens = [channelToken] #and set the first channelToken
                jingMap.put()
                return True
            else:
                return False
    
    
    success = None
    while True:
        try:
            success = registerEditor()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)

    if success:
        return {"token" : channelToken}
    else:
        return {"errorMessage" : "Service currently busy. No available task queues"}


#removes an editor from a JinglrMap. If all the editors are gone, it frees up
#the JinglrMap
def stopEditing(jid, channelToken):
    
    @ndb.transactional
    def removeEditor():
        
        #first get the JinglrMap for the specified jingle
        jm = JinglrMap.query(jingle_id == jid).fetch()
        if jm:
            #jm is a list of results containing one result
            jingMap = jm[0]
            #get tokens. This is a list of channelTokens who are editing the song
            tokens = jingMap.editor_tokens
            if channelToken in tokens:
                tokens.remove(channelToken)
                jingMap.editor_tokens = tokens  #set the updated tokens back
                if not tokens:  #if the tokens list is now empty
                    jingMap.jingle_id = None    #remove this jingle from this JignlrMap to free it up
                jingMap.put()
    
    
    while True:
        try:
            removeEditor()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)
            
            
#~~~~~~~~~~~~~~~~~~~~~~~~~ NON BLOCKING WRITES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def removeNote(jid, action):
    
    queue = getTaskqueueNameForJingle(jid)
    if queue:
        action['jid'] = jid
        action['taskqueueName'] = queue
        action = json.dumps(action)
        taskqueue.add(url = '/tasks/removenote',
                        queue_name = queue,
                        headers = {'Content-Type':'application/json'},
                        payload = action
                        )














#returns paged results with a specific ordering
def getAllJingles(order=Orderings.Date, reverse_order=False, max_results=20, cursor_url=None):
    
    jingle_query = Jingle.query()
    
    if order==Orderings.Title:
        if reverse_order:
            jingle_query=jingle_query.order(-Jingle.title, -Jingle.date_created)
        else:
            jingle_query=jingle_query.order(Jingle.title, Jingle.date_created)
            
    elif order==Orderings.Date:
        if reverse_order:
            jingle_query=jingle_query.order(-Jingle.date_created, -Jingle.title)
        else:
            jingle_query=jingle_query.order(Jingle.date_created, Jingle.title)
            
    elif order==Orderings.Rating:
        if reverse_order:
            jingle_query=jingle_query.order(-Jingle.rating, -Jingle.title)
        else:
            jingle_query=jingle_query.order(Jingle.rating, Jingle.title)
            
    elif order==Orderings.Length:
        if reverse_order:
            jingle_query=jingle_query.order(-Jingle.length, -Jingle.title)
        else:
            jingle_query=jingle_query.order(Jingle.length, Jingle.title)
            
    else:
        return None
    
    query_tuple = None
    if cursor_url:
        qc = Cursor(urlsafe=cursor_url)
        query_tuple = jingle_query.fetch_page(page_size=max_results, start_cursor=qc, projection=[Jingle.title, Jingle.author, Jingle.date_created, Jingle.genre, Jingle.length, Jingle.tags, Jingle.rating, Jingle.collab_users])
    else:
        query_tuple = jingle_query.fetch_page(page_size=max_results, projection=[Jingle.title, Jingle.author, Jingle.date_created, Jingle.genre, Jingle.length, Jingle.tags, Jingle.rating, Jingle.collab_users])
    
    cursor_string = query_tuple[1].urlsafe()
    query_tuple[1] = cursor_string
    return query_tuple
