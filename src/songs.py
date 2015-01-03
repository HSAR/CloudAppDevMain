#!/usr/bin/env python
import logging

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


class ApiSongHandler(webapp2.RequestHandler):
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
                        tags = parsed_request_json['tags']
                    result = datastore.createJingle(user_id, parsed_request_json['title'], genre, tags)
                    self.response.set_status(200)
        except ValueError:
            return error.respond(400, 'Invalid JSON in request body')


class ApiSongSidHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
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
        elif not permission.jingle_owner(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            try:
                parsed_request_json = json.loads(self.request.body)
                if not ('title' in parsed_request_json or
                                'genre' in parsed_request_json or
                                'tags' in parsed_request_json):
                    return error.respond(400, 'Missing property in request JSON')
                else:
                    result = datastore.updateJingle(songid, parsed_request_json)
                    if 'errorMessage' in result:
                        return error.respond(500, result['errorMessage'])
                    else:
                        self.response.set_status(200)
            except ValueError:
                return error.respond(400, 'Invalid JSON in request body')


class ApiSongSidJsonHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        jingle_json = datastore.getJingleJSON(songid)
        if jingle_json:
            self.response.out.write(json.dumps(jingle_json))
        else:
            return error.respond(404, "Jingle ID has no associated data")


class ApiSongSidMidiHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        else:
            jingle = datastore.getJingleJSON(songid)
            if jingle:
                try:
                    self.response.out.write(json.dumps(midi.getMIDIBase64(jingle)))
                except midi.MIDIError as exc:
                    return error.respond(500, midi.MIDIError.message)
            else:
                return error.respond(404, "Song not found.")


class ApiSongSidCollabsHandler(webapp2.RequestHandler):
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


class ApiSongSidNoteHandler(webapp2.RequestHandler):
    def delete(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
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
        elif not permission.can_edit_song(songid):
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


class ApiSongSidInstrumentHandler(webapp2.RequestHandler):
    def delete(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
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
        elif not permission.can_edit_song(songid):
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
        elif not permission.can_edit_song(songid):
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


class ApiSongSidTempoHandler(webapp2.RequestHandler):
    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
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


class ApiSongSidSubdivisionHandler(webapp2.RequestHandler):
    def put(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
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


class WebSongsSidEditorHandler(webapp2.RequestHandler):
    def get(self, songid):
        user = users.get_current_user()
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not user:
            error.respond(401, "User is not signed in")
        elif not permission.can_edit_song(songid):
            template_values = {
            }
            template = JINJA_ENVIRONMENT.get_template('templates/401.html')
            self.response.write(template.render(template_values))
        else:
            signout_bar = (
                'Signed in as %s. (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
            template_values = {
                'auth_bar': signout_bar,
                'song_id': songid,
                'song_title': datastore.getJingleById(songid).title
            }
            template = JINJA_ENVIRONMENT.get_template('templates/editor.html')
            self.response.write(template.render(template_values))


class ApiSongSidTokenHandler(webapp2.RequestHandler):
    def get(self, songid):
        self.response.headers['Content-Type'] = 'application/json'
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        elif not permission.can_edit_song(songid):
            return error.respond(401, "You are not authorised to edit this song")
        else:
            previous_token = self.request.get("prevToken")
            if not previous_token:
                request_result = datastore.beginEditing(songid)
            else:
                request_result = datastore.requestNewToken(songid, previous_token)
            if not 'token' in request_result:
                return error.respond(500, "Token request failed")
            else:
                self.response.out.write(json.dumps(request_result))
                self.response.set_status(200)


def Error404Handler(request, response, exception):
    logging.exception(exception)
    template_values = {
    }
    template = JINJA_ENVIRONMENT.get_template('templates/404.html')
    response.write(template.render(template_values))
    response.set_status(404)


def Error500Handler(request, response, exception):
    logging.exception(exception)
    template_values = {
    }
    template = JINJA_ENVIRONMENT.get_template('templates/500.html')
    response.write(template.render(template_values))
    response.set_status(500)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/api/songs', handler=ApiSongHandler,
                                                        name='songs-root'),
                                          webapp2.Route(r'/api/songs/<songid>', handler=ApiSongSidHandler,
                                                        name='state-dump'),
                                          webapp2.Route(r'/api/songs/<songid>/json', handler=ApiSongSidJsonHandler,
                                                        name='song-get-by-id'),
                                          webapp2.Route(r'/api/songs/<songid>/midi', handler=ApiSongSidMidiHandler,
                                                        name='song-get-midi-by-id'),
                                          webapp2.Route(r'/api/songs/<songid>/notes', handler=ApiSongSidNoteHandler,
                                                        name='notechanges'),
                                          webapp2.Route(r'/api/songs/<songid>/instruments',
                                                        handler=ApiSongSidInstrumentHandler,
                                                        name='instrument-changes'),
                                          webapp2.Route(r'/api/songs/<songid>/tempo', handler=ApiSongSidTempoHandler,
                                                        name='tempo-changes'),
                                          webapp2.Route(r'/api/songs/<songid>/subdivisions',
                                                        handler=ApiSongSidSubdivisionHandler,
                                                        name='subdivision-changes'),
                                          webapp2.Route(r'/api/songs/<songid>/token', handler=ApiSongSidTokenHandler,
                                                        name='editor'),
                                          webapp2.Route(r'/api/songs/<songid>/collabs',
                                                        handler=ApiSongSidCollabsHandler,
                                                        name='editor'),
                                          webapp2.Route(r'/web/songs/<songid>', handler=WebSongsSidEditorHandler,
                                                        name='editor'),
                                      ], debug=True)
application.error_handlers[404] = Error404Handler
application.error_handlers[500] = Error500Handler
					
