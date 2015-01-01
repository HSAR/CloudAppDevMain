from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import channel
from google.appengine.runtime import apiproxy_errors

import datetime
import time
import random
import string
import json
from models import JinglrUser, Jingle, JinglrMap

import taskqueue_handlers

class Orderings:
    Title, Date, Rating, Length = range(4)

#we have two entity groups. Root keys are used to define the groups
#the first group is the group of users
root_user_key = ndb.Key('UserRoot', 'userroot')
edited_jingles_key = 'Edited Jingles'

#~~~~~~~~~~~~~~~~~~~~~~~~~ INTERNAL FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#enables us to return the corresponding username for a UID on an entity so
#that clients can display the username
def getUsernameByUID(uid):
    
    username = memcache.get(uid)
    if username != None:
        return username
    else:
        user = getUserById(uid)
        if user != None:
            username = user.username
            memcache.add(uid, username, 3600)
            return username
        else:
            return None


#generates a securely random ID for use with things
def generate_id(size=32, chars=string.ascii_lowercase
                                    + string.ascii_uppercase
                                    + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


#adds a new token to the memcache
def addTokenToCache(jid, channelToken):
    
    client = memcache.Client()
    while True:
        edited_jingles = client.gets(edited_jingles_key)
        if edited_jingles == None:
            new_edited_jingles = getEditedJingles()
            if jid in new_edited_jingles:
                if channelToken not in new_edited_jingles[jid]:
                    new_edited_jingles[jid].append(channelToken)
            else:
                new_edited_jingles[jid] = [channelToken]
                
            new_edited_jingles = json.dumps(new_edited_jingles)
            
            if client.add(edited_jingles_key, new_edited_jingles, 300):
                break
        else:
            edited_jingles = json.loads(edited_jingles)
            if jid in edited_jingles:
                edited_jingles[jid].append(channelToken)
            else:
                edited_jingles[jid] = [channelToken]
            
            edited_jingles = json.dumps(edited_jingles)
            if client.cas(edited_jingles_key, edited_jingles, 300):
                break


#~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#converts a JinglrUser entity to a dictionary. The keys are the same names as
#the property names of the JinglrUser entity
def getUserDict(user):
    
    keys = ['user_id', 'username', 'bio', 'tags', 'collab_invites']
    dict = {}
    for property in keys:
        dict[property] = getattr(user, property)
    return dict


#converts a Jingle entity to a dictionary. The keys are the same names as
#the property names of the Jingle entity with the additional 'username' and
#'collab_usernames' fields
def getJingleDict(jingle, json = True):
    
    keys = ['jingle_id', 'title', 'author', 
            'genre', 'length', 'tags', 'collab_users',
            'collab_usernames']
    if json:
        keys.append('jingle')
    
    dict = {}
    for property in keys:
        dict[property] = getattr(jingle, property)
        
    date = jingle.date_created
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = date - epoch
    dict['date_created'] = delta.total_seconds()
    return dict


def getUserList(users):
    
    list = []
    for user in users:
        list.append(getUserDict(user))
    return list


def getJingleList(jingles, json = False):
    
    list = []
    for jingle in jingles:
        list.append(getJingleDict(jingle, json))
    return list


#~~~~~~~~~~~~~~~~~~~~~~~~~ READ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#takes a user id and returns the JingleUser Entity if one is found, or None
def getUserById(uid):
    
    user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
    user = user_key.get()
    if user:
        return user
    else:
        return None


#takes a username and returns the JingleUser Entity if one is found, or None
def getUserByUsername(username):
    
    user_query = JinglrUser.query(ancestor=root_user_key)
    user_query = user_query.filter(JinglrUser.username == username)
    user_list = user_query.fetch()
    if user_list:
        return user_list[0]
    else:
        return None

#returns a list of the uid and username of every registered user
def getAllUsers(all_fields):
    user_query = JinglrUser.query(ancestor=root_user_key)
    user_list = user_query.fetch()
    if user_list:
        if all_fields:
            return getUserList(user_list)
        else:
            list_of_users = []
            for user in user_list:
                list_of_users.append({"uid":user.user_id, "username":user.username})
            return list_of_users
    else:
        return None
        

#takes a user id and returns the list of jingles (possibly empty) that they
#created. It adds another property called collab_usernames which is a list of
#the usernames of the collaborators for each jingle.
def getUsersSongs(uid):
    
    jingle_query = Jingle.query(Jingle.author == uid)
    jingle_list = jingle_query.fetch()
    for jingle in jingle_list:
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
    
    return jingle_list


#takes a user id and returns the list of jingles (possibly empty) that the
#user is collaborating on. 
def getUserCollabs(uid):
    
    jingle_query = Jingle.query(Jingle.collab_users == uid)
    jingle_list = jingle_query.fetch()
    for jing in jingle_list:
        jing.username = getUsernameByUID(jing.author)
    
    for jingle in jingle_list:
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
    
    return jingle_list


#takes a user id and returns a list of jingles (possibly empty) that they have
#been invited to collaborate on. Returns None if uid is not valid
def getCollabInvites(uid):
    
    user = getUserById(uid)
    if user:
        invite_list = user.collab_invites
        jingle_list = []
        for jid in invite_list:
            current_jingle = getJingleById(jid)
            jingle_list.append(current_jingle)
        
        return jingle_list
    else:
        return None


#returns jingle entity it it exists, or None.
#It also adds a username property which is the username of the author and
#collab_usernames which is a list of the usernames of the collaborators for
#each jingle.
def getJingleById(jingle_id):
    
    jingle_key = ndb.Key('Jingle', jingle_id)
    jingle = jingle_key.get()
    
    if jingle:
        jingle.username = getUsernameByUID(jingle.author)
        
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
        
        return jingle
    else:
        return None


#returns a list of JingleUser entities who are collaborators to this Jingle.
#Returns None if jid is not valid.
def getCollaborators(jid):
    
    jingle = getJingleById(jid)
    if jingle:
        collabs_list = []
        for uid in jingle.collab_users:
            collabs_list.append(getUserById(uid))
        return collabs_list
    else:
        return None


#queries the JinglrMaps for the currently edited jingles and returns a dict
#where the keys are the jingle Ids and the values is a list of client ids
def getEditedJingles():
    
    edited_jingles = JinglrMap.query(JinglrMap.is_being_edited==True).fetch()
    edited_jingles_dict = {}
    
    for jm in edited_jingles:
        edited_jingles_dict[jm.jingle_id] = jm.tokens
        
    return edited_jingles_dict


def getJingleJSON(jid):
    
    jingle_key = ndb.Key('Jingle', jid)
    jingle = jingle_key.get()
    
    if jingle:
        return jingle.jingle
    else:
        return None


# Basic search for a jingle. Pass in a partial jingle dict with the fields to
# be searched. Note that only prefix matching will be performed, and only on
# the song name. Returns (results, cursor, more) where cursor is what's passed
# to resumeSearch and more is a flag true if there are more pages
def searchJingle(jingle, sort, isAnd):
    # Set the sort
    if "title" in jingle:
        sort = Jingle.title # limitation of datastore
    elif sort == "genre":
        sort = Jingle.genre
    elif sort == "date_created":
        sort = Jingle.date_created
    elif sort == "author":
        sort = Jingle.author
    else:
        sort = Jingle.title

    # Use AND or OR when combining items in the dict?
    if isAnd:
        combineFunction = ndb.AND
    else:
        combineFunction = ndb.OR

    # Build the query based on what was given
    query = []
    if "title" in jingle:
        query.append(ndb.AND(Jingle.title >= jingle["title"], Jingle.title < \
                jingle["title"] + u"\ufffd"))
    if "author" in jingle:
        query.append(Jingle.author == jingle["author"])
    if "genre" in jingle:
        query.append(Jingle.genre == jingle["genre"])
    if "tags" in jingle:
        query.append(Jingle.tags == jingle["tags"])

    # Apply the query. Two special cases of length 0 and 1.
    if len(query) == 0:
        jingle_query = Jingle.query().order(sort, Jingle.key)
    elif len(query) == 1:
        jingle_query = Jingle.query(query[0]).order(sort, Jingle.key)
    else:
        jingle_query = Jingle.query(combineFunction(*query)).order(sort,
                Jingle.key)

    results, cursor, more = jingle_query.fetch_page(10)

    jingleDicts = []

    for jingle in results: # results
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
        jingleDicts.append(getJingleDict(jingle, False))

    return (jingleDicts, cursor, more)

# Resume search by passing a cursor (second item in returned tuple from search)
# Returns same as searchJingle
def resumeSearch(cursor):
    results, cursor, more = Jingle.query().fetch_page(10, start_cursor=cursor)

    jingleDicts = []
    for jingle in results: # results
        username_list = []
        for user_id in jingle.collab_users:
            username_list.append(getUsernameByUID(user_id))
        jingle.collab_usernames = username_list
        jingleDicts.append(getJingleDict(jingle, False))
    
    return (jingleDicts, cursor, more)


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
                        tags=[],
                        collab_invites=[]
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
        except (db.Timeout, db.TransactionFailedError, db.InternalError):
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
        
        user = getUserById(uid)
        
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
        except (db.Timeout, db.TransactionFailedError, db.InternalError):
            time.sleep(1)
    
    return result


#takes a user id and a new bio. Returns the user entity key on success or None
#if that user does not exist
def updateBio(uid, bio):
    
    while True:
        try:
            user = getUserById(uid)
            if not user:
                return None
            
            user.bio = bio
            return user.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


#takes a user ID and a new list of tags. Returns the user entity key on
#success or None if that user does not exist
def updateTags(uid, tags):
    
    while True:
        try:
            user = getUserById(uid)
            if not user:
                return None
            
            user.tags = tags
            return user.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


#takes a username and the JID that this user is being invited to collab on
#returns a python dictionary. If there was an error:
#    {"errorMessage" : errorMessage}
#or on success:
#    {"userKey" : key}
#userKey is the JinglrUser entity key for the updated user entity
def addCollabInvite(username, jid):
    
    @ndb.transactional
    def addCollabInviteInternal():
        jingle = getJingleById(jid)
        if jingle:
            user = getUserByUsername(username)
            if user:
                user.collab_invites.append(jid)
                user_key = user.put()
                
                return {"userKey" : user_key}
            else:
                return {"errorMessage" : "No user has that username"}
        else:
            return {"errorMessage" : "Invalid Jingle"}
    
    result = None
    while True:
        try:
            result = addCollabInviteInternal()
        except (db.Timeout, db.InternalError, db.TransactionFailedError):
            time.sleep(1)
    return result


#accept - a boolean. If true the invite is accepted, otherwise rejected
#if it is true it adds the users uid to the corresponding jingle
#the invite is removed once answered
#returns a python dictionary. If there was an error:
#    {"errorMessage" : errorMessage}
#or on success:
#    {"userKey" : key}
#userKey is the JinglrUser entity key for the updated user entity
def answerCollabInvite(uid, jid, accept):
    
    @ndb.transactional(xg=True)
    def answerCollabInviteInternal():
        user = getUserByID(uid)
        if user:
            if jid in user.collab_invites:
                if accept:
                    jingle_key = ndb.Key('Jingle', jid)
                    jingle = jingle_key.get()
                    jingle.collab_users.append(uid)
                    jingle.put()
                    
                user = getUserByID(uid)
                user.collab_invites.remove(jid)
                user_key = user.put()
                
                return {"userKey" : user_key}
            else:
                return {"errorMessage" : "You have not been invited to " +
                            "collaborate on this jingle"}
        return {"errorMessage" : "Invalid user"}

    result = None
    while True:
        try:
            result = answerCollabInviteInternal()
        except (db.Timeout, db.InternalError, db.TransactionFailedError):
                    time.sleep(1)
    return result


#this is used to stop a particular user collaborating on a particular song.
#may be called when a user wants to stop collaborating on a song or a song
#author wants to remove a collaborator
#returns a python dictionary. If there was an error:
#    {"errorMessage" : errorMessage}
#or on success:
#    {"jingleKey" : key}
#jingleKey is the Jingle entity key for the updated Jingle entity
def removeCollab(uid, jid):
    
    @ndb.transactional
    def removeCollabInternal():
        jingle_key = ndb.Key('Jingle', jid)
        jingle = jingle_key.get()
        if jingle:
            if uid in jingle.collab_users:
                jingle.collab_users.remove(uid)
                jingle_key = jingle.put()
                return {"jingleKey" : jingle_key}
            else:
                return {"errorMessage" : "User is not collaborating" +
                                             " on the jingle"}
        else:
            return {"errorMessage" : "Invalid Jingle ID"}
            
    result = None
    while True:
        try:
            result = removeCollabInternal()
        except (db.Timeout, db.InternalError, db.TransactionFailedError):
            time.sleep(1)
    return result

    
#takes stuff to create a jingle entity
#returns new jingle entity key once successful
def createJingle(uid, title, genre=None, tags=None):
    
    gen_id = generate_id();
    
    jingle = Jingle(id=gen_id, jingle_id=gen_id, title=title, author=uid)
    if genre:
        jingle.genre = genre
    if tags:
        jingle.tags = tags
    else:
        jingle.tags = []
    
    jingle_json = {}
    jingle_json['head'] = {'subDivisions':8, 'tempo':120, 'barLength':4}
    jingle_json['tracks'] = []
    for i in range(0,15):
        jingle_json['tracks'].append({})
    jingle.jingle = jingle_json
    
    jingle.collab_users = []
    
    result = None
    while True:
        try:
            result = jingle.put()
            
            map_name = gen_id + 'Map'
            jm = JinglrMap(id=map_name, jingle_id=gen_id, client_ids = [],
                           tokens = [])
            jm.put()
            break
        except (db.Timeout, db.InternalError):
            time.sleep(1)
    
    return result


#returns the Jingle entity key on success, or None if jid is not valid
def changeTitle(jid, title):
    
    while True:
        try:
            jingle_key = ndb.Key('Jingle', jid)
            jingle = jingle_key.get()
            if not jingle:
                return None
            
            jingle.title = title
            return jingle.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


#returns the Jingle entity key on success, or None if jid is not valid
def changeGenre(jid, genre):
    
    while True:
        try:
            jingle_key = ndb.Key('Jingle', jid)
            jingle = jingle_key.get()
            if not jingle:
                return None
                
            jingle.genre = genre
            return jingle.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


#returns the Jingle entity key on success, or None if jid is not valid
def changeTags(jid, tags):
    
    while True:
        try:
            jingle_key = ndb.Key('Jingle', jid)
            jingle = jingle_key.get()
            if not jingle:
                return None
            
            jingle.tags = tags 
            return jingle.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


def changeJingle(jid, jingle_json):
    
    while True:
        try:
            jingle_key = ndb.Key('Jingle', jid)
            jingle = jingle_key.get()
            if not jingle:
                return None
            
            jingle.jingle = jingle_json
            return jingle.put()
        except (db.Timeout, db.InternalError):
            time.sleep(1)


#called when a client wants to start editing a jingle
#in a success case it will return:
#   {"token" : channelToken}
#in a fail (because we went over our channel quota) it will return:
#   {"errorMessage" : errorMessage}
def beginEditing(jid):
    #first get the JinglrMap entity for this Jingle
    jm = ndb.Key('JinglrMap', jid+'Map').get()
    if not jm:
        return {"errorMessage" : "Invalid Jingle ID"}
    
    #next try to create a channel token using a randomly generated client ID
    channelToken = None
    client_id = generate_id()
    try:
        channelToken = channel.create_channel(client_id)
    except apiproxy_errors.OverQuotaError:
        return {"errorMessage" : "Channels quota met: no more channels"}
    
    #now update persistent storage with the new client ID
    @ndb.transactional
    def registerEditor():
        
        jm = ndb.Key('JinglrMap', jid+'Map').get()
        if not jm:
            return False
        
        jm.client_ids.append(client_id)
        jm.tokens.append(channelToken)
        jm.put()
        return True
    
    success = None
    while True:
        try:
            success = registerEditor()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError):
            time.sleep(1)
    
    #now update memcache with the new value
    #{edited_jingles_key : {jid1 : [client_id_list], jid2 : [client_id_list]}}
    if success:
        addTokenToCache(jid, channelToken)
                    
        taskqueue_handlers.makeSureTaskHandlerIsRunning()
        
        return {"token" : channelToken}
    else:
        return {"errorMessage" : "Invalid Jingle ID"}


#called when a client needs a new token because their current one expired
#takes the jid of the jingle they are editing and their old token
#in a success case it will return:
#   {"token" : channelToken}
#in a fail it will return:
#   {"errorMessage" : errorMessage}
def requestNewToken(jid, old_token):
    
    new_client_ID = None
    new_token = None
    jm_key = ndb.Key('JinglrMap', jid+'Map')
    if jm_key.get():
        new_client_ID = generate_id()
        try:
            new_token = channel.create_channel(new_client_ID)
        except apiproxy_errors.OverQuotaError:
            return {"errorMessage" : "Channels quota met: no more channels"}
    else:
        return {"errorMessage" : "Invalid jid"}
    
    @ndb.transactional
    def newToken(jm_key, ncid, nt):
        jm = jm_key.get()
        if old_token in jm.tokens:
            index = jm.tokens.index(old_token)
            client_id = jm.client_ids[index]
            jm.client_ids.remove(client_id)
            jm.tokens.remove(old_token)
        
        jm.client_ids.append(ncid)
        jm.tokens.append(nt)
        
        jm.put()
    
    while True:
        try:
            newToken(jm_key, new_client_ID, new_token)
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError):
            time.sleep(1)
    
    addTokenToCache(jid, new_token)
        
    return {"token" : new_token}


#removes an editor from a JinglrMap.
def stopEditing(client_id):
    
    @ndb.transactional
    def removeEditor(jm_key):
        jm = jm_key.get()
        if client_id in jm.client_ids:
            index = jm.client_ids.index(client_id)
            jm.client_ids.remove(client_id)
            token = jm.tokens[index]
            jm.tokens.remove(token)
            jm.put()
    
    
    jinglr_query = JinglrMap.query(JinglrMap.client_ids == client_id)
    jinglr_list = jinglr_query.fetch()
    
    if len(jinglr_list) > 0:
        jm = jinglr_list[0]
 
        while True:
            try:
                removeEditor(jm.key)
                break
            except (db.Timeout, db.TransactionFailedError, db.InternalError):
                time.sleep(1)


#~~~~~~~~~~~~~~~~~~~~~~~~~ NON BLOCKING WRITES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#submits an action to processed on a jingle json. jid is the id of the jingle
#to be edited and action is a dictionary of the action as defined in protocols
def submitAction(jid, action):
    
    client = memcache.Client()
    while True:
        actionList = client.gets(jid)
        if actionList == None:
            val = json.dumps([action])
            if client.add(jid, val):
                break
        else:
            actionList = json.loads(actionList)
            actionList.append(action)
            actionList = json.dumps(actionList)
            if client.cas(jid, actionList):
                break



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
