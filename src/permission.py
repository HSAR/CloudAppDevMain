#!/usr/bin/env python
#
# This class is used to check whether a user can edit a particular song.
#

import datastore

from google.appengine.api import users

def allowed(song_id):

    #user is author, or user is collaborator
    #user_id = users.get_current_user().user_id()
    #jigle_list = datastore.getUsersSongs(user_id)
    #jingle_list.extend(datastore.getUsersCollabs(user_id))
    #for jingle in jingle_list:
    #    if jingle.jingle_id == song_id
    #        return True
    #return False
    
    user_id = users.get_current_user().user_id()
    jingle = datastore.getJingleById(song_id)
    if jingle and (jingle.author == user_id or user_id in jingle.collab_users):
        return True
    return False
