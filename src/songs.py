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

class SongGetHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            self.abort(400)
        jingle_json = datastore.getJingleJSON(songid)
        if jingle_json:
            self.response.out.write(json.dumps(jingle_json))
        else:
            return error.respond("404", "Jingle ID has no associated data")


class SongGetMidiHandler(webapp2.RequestHandler):
    def get(self, songid):
        #if not songid:
            self.abort(400)
        # datastore not working
        # jingle = datastore.getJingleById(songid)
        # hardcode songs for testing
        #jingle = None
        #if songid == "0":
        #    jingle = song0
        #elif songid == "1":
        #    jingle = song1
        #if jingle:
        #    try:
        #        #self.response.out.write(midi.getMIDIBase64(json.dumps(jingle.jingle)))
        #        self.response.out.write(midi.getMIDIBase64(json.dumps(jingle)))
        #    except midi.MIDIError as exc:
        #        raise exc
        #        self.response.out.write(midi.MIDIError.message)
        #        self.abort(500)
        #else:
        #    self.abort(404)


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
                if not (('note' in parsed_request_json) and ('actionId' in parsed_request_json)):
                    return error.respond(400, 'Missing property in request JSON')
                elif not ('id' in parsed_request_json['note'] and 'pos' in parsed_request_json['note'] and 'track' in
                    parsed_request_json['note'] and 'note' in parsed_request_json['note'] and 'length' in
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
                if not ('instrument' in parsed_request_json and 'actionId' in parsed_request_json):
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


class EditorPageHandler(webapp2.RequestHandler):
    def get(self, songid):
        user = users.get_current_user()
        if user:
            signout_bar = (
                'Signed in as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
            template_values = {
                'auth_bar': signout_bar,
                'song_id': songid
            }
            template = JINJA_ENVIRONMENT.get_template('templates/editor.html')
            datastore.beginEditing(songid)
            self.response.write(template.render(template_values))
        else:
            error.respond(401, "User is not signed in")


application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/songs/<songid>', handler=SongGetHandler,
                                                        name='song-get-by-id'),
                                          webapp2.Route(r'/songs/<songid>/midi', handler=SongGetMidiHandler,
                                                        name='song-get-midi-by-id'),
                                          webapp2.Route(r'/songs/<songid>/notes', handler=NoteChangeHandler,
                                                        name='notechanges'),
                                          webapp2.Route(r'/songs/<songid>/instruments', handler=InstrumentChangeHandler,
                                                        name='instrument-changes'),
                                          webapp2.Route(r'/songs/<songid>/editor', handler=EditorPageHandler,
                                                        name='editor'),
                                      ], debug=True)
					
