from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users

import datetime
from models import JinglrUser, Jingle

class Orderings:
	Title, Date, Rating, Length = range(4)
		
class UnsupportedActionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
	
class Datastore:
	
	root_key = ndb.Key('Root', 'root')
	
	def __init__(self):
		self.queue = None
	
	def set_queue(self, queue):
		self.queue = queue
	
	def generate_jingle_id(self, uid, title, timestamp):
		return uid+title+timestamp
	
	def createUser(self, user_object, username=None):

		ju = JinglrUser(parent=root_key, id=user_object.user_id(), 
										user_id=user_object.user_id(), 
										username=user_object.nickname()
										)
		if username:
			ju.username = username
		return ju.put()
		
	def getUserById(self, uid):
			
		user_key = ndb.Key('JinglerUser', uid, parent=root_key)
		user = user_key.get()
		if user:
			return user
		else:
			return None
			
	def getUserByUsername(self, username):

		user_query = JinglrUser.query(ancestor=root_key).filter(JinglrUser.username == username)
		user_list = user_query.fetch()
		if user_list:
			return user_list[1]
		else:
			return None
		
	def updateUsername(self, uid, username):

		user_key = ndb.Key('JinglerUser', uid, parent=root_key)
		user = user_key.get()
		if user:
			user.username = username
			return user.put()
		else:
			return None
			
	def updateBio(self, uid, bio):

		user_key = ndb.Key('JinglerUser', uid, parent=root_key)
		user = user_key.get()
		if user:
			user.bio = bio
			return user.put()
		else:
			return None
			
	def updateTags(self, uid, tags):
		
		user_key = ndb.Key('JinglerUser', uid, parent=root_key)
		user = user_key.get()
		if user:
			user.tags = tags
			return user.put()
		else:
			return None

	def createJingle(self, uid, title, genre=None, tags=None):
		
		timestamp=datetime.datetime.now()
		gen_id = self.generate_jingle_id(uid, title, str(timestamp))
		
		jingle = Jingle(id=title, jingle_id=gen_id, title=title, author=user_object.user_id())
		if genre:
			jingle.genre = genre
		if tags:
			jingle.tags = tags
		
		jingle_key = jingle.put()
		
	def getJingleById(self, jingle_id):
		
		jingle_key = ndb.Key('Jingle', jingle_id)
		jingle = jingle_key.get()
		if jingle:
			return jingle
		else:
			return None	
	
	def getAllJingles(self, order=Orderings.Date, reverse_order=False, max_results=20, cursor_url=None):
		
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
		
	def test_dispatch(self, arg1, arg2):
		return arg1+arg2
	
	def dispatch_write_operation(self, operation, **kwargs):
	
		operation_name = operation
		operation_args = kwargs
		
		if hasattr(self, operation):
			method = getattr(self, operation)
			
			#queue operation
			
		else:
			raise UnsupportedOperationException("This operation is not supported")