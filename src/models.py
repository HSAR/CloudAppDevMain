from google.appengine.ext import ndb

class JinglrUser(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    bio = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    collab_invites = ndb.StringProperty(repeated=True)
    
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
    jingle_id = ndb.StringProperty(required=True)
    editor_tokens = ndb.StringProperty(repeated=True)
    is_being_edited = ndb.ComputedProperty(lambda self: len(self.editor_tokens) == 0)
