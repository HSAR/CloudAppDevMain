from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users

import datetime
import time
from google.appengine.api import channel
from models import JinglrUser, Jingle, JinglrMap
from google.appengine.

class Orderings:
	Title, Date, Rating, Length = range(4)
		
#we have two entity groups. Root keys are used to define the groups
#the first group is the group of users
root_user_key = ndb.Key('UserRoot', 'userroot')
#the second group is the group of jinglr maps
root_jinglrmap_key = ndb.Key('JinglrMapRoot', 'jinglrmaproot')

def generate_jingle_id(uid):
    
    timestamp = datetime.datetime.now()
    rand = random.random()
	return uid + str(rand) + str(timestamp)

#takes a uid and a username
#returns a dictionary.
#if there was an error:
    #{"error" : errorMessage}
#if successful:
    #{"userKey" : userKey}
def createUser(uid, username):
    
    @ndb.transactional
    def createUserInternal():
        
        existingUser = getUserByUsername(username)
        
        if existingUser:
            return {"errorMessage":"That username has already been taken"}
            
        existingUser = getUserById(uid)
        
        if existingUser:
            return {"errorMessage":"You have already registered an account"}
        
        ju = JinglrUser(parent=root_user_key, 
                        id=uid, 
                        user_id=uid, 
                        username=username
                       )
        
        result = ju.put()
        return {"userKey":result}
    
    
    if !username:
        return {"errorMessage":"Please enter a username"}
    
    result = None
    
    while True:
        try:
            result = createUserInternal()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)
    
    return result

#takes a user id and returns the JingleUser Entity if one is found, or None
def getUserById(uid):
    
	user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
	user = user_key.get()
	if user:
		return user
	else:
		return None

#takes a username and returns the JingleUser Entity if one is foind, or None
def getUserByUsername(username):
    
	user_query = JinglrUser.query(ancestor=root_user_key).filter(JinglrUser.username == username)
	user_list = user_query.fetch()
	if user_list:
		return user_list[0]
	else:
		return None

#takes a user ID and a new username
#returns a dictionary in the form:
#   {"userKey" : userkey}
#when successful or:
#   {"errorMessage" : errorMessage}
#on a fail          
def updateUsername(uid, username):
    
    if !username:
        return {"errorMessage":"Please enter a username"}
    
    user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
	user = user_key.get()
    
    if !user:
        return {"errorMessage" : "That is not a valid user"}
    
    @ndb.transactional
    def updateUsernameInternal():
        
        existingUser = getUserByUsername(username)
        
        if existingUser:
            return {"errorMessage" : "That username has already been taken"}
        
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
    
	user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
	user = user_key.get()
	if user:
        result = None
        while True:
            try:
                user.bio = bio
                result = user.put()
                break
            except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                time.sleep(1)
		
		return result
	else:
		return None

#takes a user ID and a new list of tags. Returns the user entity key on success
#or None if that user does not exist
def updateTags(uid, tags):
	
	user_key = ndb.Key('JinglrUser', uid, parent=root_user_key)
	user = user_key.get()
	if user:
        result = None
        while True:
            try:
                user.tags = tags
                result = user.put()
                break
            except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
                time.sleep(1)
		
		return result
	else:
		return None

#takes stuff to create a jingle entity
#returns new jingle entity key once successful
def createJingle(uid, title, genre=None, tags=None):
	
	gen_id = self.generate_jingle_id(uid)
	
	jingle = Jingle(id=gen_id, jingle_id=gen_id, title=title, author=uid)
	if genre:
		jingle.genre = genre
	if tags:
		jingle.tags = tags
	
    result = None
    while True:
        try:
            result = jingle.put()
            break
        except (db.Timeout, db.TransactionFailedError, db.InternalError) as exep:
            time.sleep(1)
    
    return result

#returns jingle entity it it exists, or None
def getJingleById(jingle_id):
	
	jingle_key = ndb.Key('Jingle', jingle_id)
	jingle = jingle_key.get()
	if jingle:
		return jingle
	else:
		return None	

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
	
#Get the name of the task queue allocated to the jingle, or None if there isn't one
def taskqueueNameForJingle(jid):
	
	map_query = JinglrMap.query(jingle_id==jid)
	jm = map_query.fetch()
	if jm:
		return jm[0].taskqueue_name
	else:
		return None

def beginEditing(uid, jid):
    
	channeltoken = channel.create_channel(uid)
	
	@ndb.transactional
	def register_editor(jingleid, token):
	
		jm = JinglrMap.query(jingle_id==jingleid).fetch()
		if not jm:
			jm = JinglrMap.query(jingle_id=None).fetch()
			if jm:
				jm.jingle_id = jingleid
			else:
				#No taskqueue available, abort
		
		jm.current_editors += 1
		jm.editor_tokens.append(token)
		jm.put()
		
	register_editor(jid, channeltoken)
	
	return token