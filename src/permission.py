#!/usr/bin/env python
#
# This class is used to check whether a user can edit a particular song.
#

import datastore

from google.appengine.api import users

def allowed(song_id):
    user_id = users.get_current_user().user_id()
    result = datastore.getCollabInvites(user_id)
    return song_id in result
