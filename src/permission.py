#!/usr/bin/env python
#
# This class is used to check whether a user is allowed to perform a particular action
#

import datastore

from google.appengine.api import users

# only the jingle author or collaborator can edit the jingles song
def can_edit_song(song_id):
    user = users.get_current_user()
    if user:
        user_id = user.user_id()
        jingle = datastore.getJingleById(song_id)
        if user.email() == 'jinglrsoton@gmail.com':
            return True
        else:
            return jingle and (jingle.author == user_id or user_id in jingle.collab_users)
    else:
        return False


#users are only able to edit themselves
def can_edit_user(uid):
    user = users.get_current_user()
    if user:
        user_id = user.user_id()
        return uid == user_id
    else:
        return False


#only the jingle author can invite people to collaborate and change the jingles
#title, genre and tags
def jingle_owner(song_id):
    user = users.get_current_user()
    if user:
        user_id = user.user_id()
        jingle = datastore.getJingleById(song_id)
        if jingle:
            return jingle.author == user_id
        else:
            return False
    else:
        return False


#users can only remove themselves from collaborating on a particular jingle
#jingle authors can remove any collaborator from it
def can_remove_collab(song_id, user_id):
    user = users.get_current_user()
    if user:
        current_user = user.user_id()
        jingle = datastore.getJingleById(song_id)
        if jingle:
            return jingle.author == current_user or current_user == user_id
        else:
            return False
    else:
        return False


#only registered users are able to perform certain actions
def is_registered():
    user = users.get_current_user()
    if user:
        current_user = user.user_id()
        return datastore.getUserById(current_user) is not None
    else:
        return False