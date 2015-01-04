from google.appengine.ext import ndb

# This file defines the structure of the entities used in our datastore
# JinglrUser contains details on registered users
#Each Jingle entity stores the details for a particular song
#Each Jingle also has a corresponding JinglrMap which is used to keep track
#of which clients are currently editing the Jingle
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
    collab_users = ndb.StringProperty(repeated=True)


class JinglrMap(ndb.Model):
    jingle_id = ndb.StringProperty(required=True)
    client_ids = ndb.StringProperty(repeated=True)
    tokens = ndb.StringProperty(repeated=True)
    is_being_edited = ndb.ComputedProperty(lambda self: len(self.client_ids) != 0)
