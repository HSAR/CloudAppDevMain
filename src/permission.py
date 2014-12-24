#!/usr/bin/env python
#
# This class is used to check whether a user can edit a particular song.
#

import datastore

from google.appengine.api import users

def allowed(song_id):
    
    user = users.get_current_user()
    if user:
        user_id = user.user_id()
        jingle = datastore.getJingleById(song_id)
        return jingle and (jingle.author == user_id or user_id in jingle.collab_users)
    else:
        return False
