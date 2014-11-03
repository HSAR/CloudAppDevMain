from google.appengine.ext import ndb

class JinglrUser(ndb.Model):
	user_id = ndb.StringProperty(required=True)
	username = ndb.StringProperty(required=True)
	number_of_songs = ndb.IntegerProperty()
	bio = ndb.TextProperty()
	tags = ndb.StringProperty(repeated=True) #I'm still not entirely convinced that tags for a user are worth the trouble
	
class Jingle(ndb.Model):
	title = ndb.StringProperty(required=True)
	genre = ndb.StringProperty()
	length = ndb.IntegerProperty(required=True) #Seconds, I'm guessing
	tags = ndb.StringProperty(repeated=True)
	jingle = ndb.JsonProperty(required=True)
	rating = ndb.FloatProperty()