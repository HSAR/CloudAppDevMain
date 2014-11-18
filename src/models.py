from google.appengine.ext import ndb

class JinglrUser(ndb.Model):
	user_id = ndb.StringProperty(required=True)
	username = ndb.StringProperty(required=True)
	bio = ndb.TextProperty()
	tags = ndb.StringProperty(repeated=True)
	collab_songs = ndb.StringProperty(repeated=True)
	
class Jingle(ndb.Model):
	jingle_id = ndb.StringProperty(required=True)
	title = ndb.StringProperty(required=True)
	author = ndb.StringProperty(required=True)
	date_created = ndb.DateTimeProperty(auto_now_add=True)
	genre = ndb.StringProperty()
	length = ndb.IntegerProperty()
	tags = ndb.StringProperty(repeated=True)
	jingle = ndb.JsonProperty()
	#rating = ndb.FloatProperty()
	collab_users = ndb.StringProperty(repeated=True)
    
class JinglrMap(ndb.Model):
    taskqueue_name = nbd.StringProperty(required=True)
    jingle_id = ndb.StringProperty()
    editor_tokens = nbd.StringProperty(repeated=True)
    map_id = ndb.IntegerProperty(required=True)