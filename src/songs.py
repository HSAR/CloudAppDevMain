#!/usr/bin/env python

import os
import datetime

import webapp2
import jinja2

import json

import datastore
import permission
import error
import midi

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class SongRootHandler(webapp2.RequestHandler):
    # this will eventually contain searching, I think
    def put(self):
        try:
            parsed_request_json = json.loads(self.request.body)
            if not ('title' in parsed_request_json):
                return error.respond(400, 'Missing property in request JSON')
            else:
                user = users.get_current_user()
                if not user:
                    return error.respond(401, "You are not signed in")
                else:
                    user_id = user.user_id()
                    genre = None
                    tags = None
                    if 'genre' in parsed_request_json:
                        genre = parsed_request_json['genre']
                    if 'tags' in parsed_request_json:
                        genre = parsed_request_json['tags']
                    result = datastore.createJingle(user_id, parsed_request_json['title'], genre, tags)
                    self.response.write(json.dumps(result))
                    self.response.set_status(200)
        except ValueError:
            return error.respond(400, 'Invalid JSON in request body')


class SongDataHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            result = datastore.getJingleById(songid)
            if result:
                self.response.write(json.dumps(datastore.getJingleDict(result)))
                self.response.set_status(200)
            else:
                return error.respond(404, "No song found with this ID")

    def patch(self, songid):
        if not songid:
            return error.respond(400, "Invalid user ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('title' in parsed_request_json or
                                'genre' in parsed_request_json or
                                'tags' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                else:
                    success = True
                    if 'title' in parsed_request_json:
                        result = datastore.changeTitle(songid, parsed_request_json['title'])
                        success &= result
                    if 'genre' in parsed_request_json:
                        result = datastore.updateBio(songid, parsed_request_json['genre'])
                        success &= result
                    if 'tags' in parsed_request_json:
                        result = datastore.updateTags(songid, parsed_request_json['tags'])
                        success &= result
                    if not success:
                        return error.respond(500, "One or more failures encountered while executing field updates")
                    else:
                        self.response.write(json.dumps(result))
                        self.response.set_status(200)
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class SongGetJSONHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        jingle_json = datastore.getJingleJSON(songid)
        if jingle_json:
            self.response.out.write(json.dumps(jingle_json))
        else:
            return error.respond(404, "Jingle ID has no associated data")


class SongGetMidiHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        else:
            jingle = datastore.getJingleJSON(songid)
            if jingle:
                try:
                    self.response.out.write(midi.getMIDIBase64(json.dumps(
                        jingle)))
                except midi.MIDIError as exc:
                    return error.respond(500, midi.MIDIError.message)
            else:
                return error.respond(404, "Song not found.")


class SongCollaboratorsHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        else:
            result = datastore.getCollaborators(songid)
            if result is not None:
                self.response.write(json.dumps(datastore.getUserList(result)))
                self.response.set_status(200)
            else:
                return error.respond(404, "No song found with this ID")


class NoteChangeHandler(webapp2.RequestHandler):
    def delete(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            action_id = self.request.get("actionId")
            track = self.request.get("track")
            note_id = self.request.get("noteId")
            if action_id and track and note_id:
                try:
                    track = int(track)
                except ValueError:
                    return error.respond(400, "Invalid request parameter(s)")
                datastore_request_object = {
                    'action': 'noteRm',
                    'actionId': action_id,
                    'track': track,
                    'noteId': note_id
                }
                datastore.submitAction(songid, datastore_request_object)
                success_object = {
                    'status': 'true',
                }
                self.response.write(json.dumps(success_object))
                self.response.set_status(200)
                return
            else:
                return error.respond(400, 'Missing request parameter(s)')

    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('action' in parsed_request_json and
                                'note' in parsed_request_json and
                                'actionId' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                elif not ('id' in parsed_request_json['note'] and 'pos' in parsed_request_json['note'] and 'track' in
                    parsed_request_json['note'] and 'pitch' in parsed_request_json['note'] and 'length' in
                    parsed_request_json['note']):
                    return error.respond(400, 'Missing property in request JSON note object')
                else:
                    datastore.submitAction(songid, parsed_request_json)
                    success_object = {
                        'status': 'true',
                    }
                    self.response.write(json.dumps(success_object))
                    self.response.set_status(200)
                    return
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class InstrumentChangeHandler(webapp2.RequestHandler):
    def delete(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            action_id = self.request.get("actionId")
            instrument_track = self.request.get("instrumentTrack")
            if action_id and instrument_track:
                try:
                    instrument_track = int(instrument_track)
                except ValueError:
                    return error.respond(400, "Invalid request parameter(s)")
                datastore_request_object = {
                    'action': 'instrumentRm',
                    'actionId': action_id,
                    'instrumentTrack': instrument_track,
                }
                datastore.submitAction(songid, datastore_request_object)
                success_object = {
                    'status': 'true',
                }
                self.response.write(json.dumps(success_object))
                self.response.set_status(200)
                return
            else:
                return error.respond(400, 'Missing request parameter(s)')

    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('action' in parsed_request_json and
                                'instrument' in parsed_request_json and
                                'actionId' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                elif not ('track' in parsed_request_json['instrument'] and 'inst' in parsed_request_json['instrument']):
                    return error.respond(400, 'Missing property in request JSON note object')
                else:
                    datastore.submitAction(songid, parsed_request_json)
                    success_object = {
                        'status': 'true',
                    }
                    self.response.write(json.dumps(success_object))
                    self.response.set_status(200)
                    return
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')

    def patch(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('action' in parsed_request_json and
                                'actionId' in parsed_request_json and
                                'instrumentTrack' in parsed_request_json and
                                'instrumentNumber' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                else:
                    datastore.submitAction(songid, parsed_request_json)
                    success_object = {
                        'status': 'true',
                    }
                    self.response.write(json.dumps(success_object))
                    self.response.set_status(200)
                    return
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class TempoChangeHandler(webapp2.RequestHandler):
    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('action' in parsed_request_json and
                                'tempo' in parsed_request_json and
                                'actionId' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                else:
                    datastore.submitAction(songid, parsed_request_json)
                    success_object = {
                        'status': 'true',
                    }
                    self.response.write(json.dumps(success_object))
                    self.response.set_status(200)
                    return
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class SubdivisionChangeHandler(webapp2.RequestHandler):
    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('action' in parsed_request_json and
                                'subDivisions' in parsed_request_json and
                                'actionId' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                else:
                    datastore.submitAction(songid, parsed_request_json)
                    success_object = {
                        'status': 'true',
                    }
                    self.response.write(json.dumps(success_object))
                    self.response.set_status(200)
                    return
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class EditorPageHandler(webapp2.RequestHandler):
    def get(self, songid):
        user = users.get_current_user()
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not user:
            error.respond(401, "User is not signed in")
        else:
            signout_bar = (
                'Signed in as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
            template_values = {
                'auth_bar': signout_bar,
                'song_id': songid
            }
            template = JINJA_ENVIRONMENT.get_template('templates/editor.html')
            self.response.write(template.render(template_values))


class BeginEditing(webapp2.RequestHandler):
    def get(self, songid):
        self.response.headers['Content-Type'] = 'application/json'
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.allowed(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            request_result = datastore.beginEditing(songid)
            if not 'token' in request_result:
                return error.respond(500, "Token request failed")
            else:
                self.response.out.write(json.dumps(request_result))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/songs/', handler=SongRootHandler,
                                                        name='songs-root'),
                                          webapp2.Route(r'/songs/<songid>/', handler=SongDataHandler,
                                                        name='state-dump'),
                                          webapp2.Route(r'/songs/<songid>/json', handler=SongGetJSONHandler,
                                                        name='song-get-by-id'),
                                          webapp2.Route(r'/songs/<songid>/midi', handler=SongGetMidiHandler,
                                                        name='song-get-midi-by-id'),
                                          webapp2.Route(r'/songs/<songid>/notes', handler=NoteChangeHandler,
                                                        name='notechanges'),
                                          webapp2.Route(r'/songs/<songid>/instruments', handler=InstrumentChangeHandler,
                                                        name='instrument-changes'),
                                          webapp2.Route(r'/songs/<songid>/tempo', handler=TempoChangeHandler,
                                                        name='tempo-changes'),
                                          webapp2.Route(r'/songs/<songid>/subdivisions',
                                                        handler=SubdivisionChangeHandler,
                                                        name='subdivision-changes'),
                                          webapp2.Route(r'/songs/<songid>/token', handler=BeginEditing,
                                                        name='editor'),
                                          webapp2.Route(r'/songs/<songid>/editor', handler=EditorPageHandler,
                                                        name='editor'),
                                          webapp2.Route(r'/songs/<songid>/collabs', handler=SongCollaboratorsHandler,
                                                        name='editor'),
                                      ], debug=True)
					
