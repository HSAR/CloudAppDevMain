#!/usr/bin/env python

import os
import datetime

import webapp2
import jinja2

import json

import datastore
import error

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import channel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

song0 = {  # this song is just a C major scale, but with notes alternating between crotchets and quavers.
           "head":
               {
                   "subdivisions": 16,
                   "tempo": 120,
                   "title": "Zubion",
                   "bars": 6,  # what the hell is this measured in? Beats? I'm guessing beats.
                   "genre": "French",
                   "tags": ["ou", "est", "la", "gare"],
                   "id": 0,
                   "barLength": 4
               },
           "tracks":
               [
                   {
                       "instrument": 0,  # acoustic grand piano
                       "notes":
                           [
                               {
                                   "id": "note-24e7f3c5-d2f0-4e40-aae0-3e687d901bde",
                                   "position": 0,
                                   "length": 16,
                                   "pitch": 60,
                               },
                               {
                                   "id": "note-78a06d95-97e1-44cd-9175-e4617a1a206a",
                                   "position": 16,
                                   "length": 8,
                                   "pitch": 62,
                               },
                               {
                                   "id": "note-635fbf94-a45a-4b90-940c-a5cf245ccdac",
                                   "position": 24,
                                   "length": 16,
                                   "pitch": 64,
                               },
                               {
                                   "id": "note-f36f02d5-6da8-4459-9c01-014efcffe56e",
                                   "position": 40,
                                   "length": 8,
                                   "pitch": 65,
                               },
                               {
                                   "id": "note-9ec8b033-0f4b-4688-b6f1-42782964dcaf",
                                   "position": 48,
                                   "length": 16,
                                   "pitch": 67,
                               },
                               {
                                   "id": "note-4a3320b5-0c60-4766-9d09-8a272e0afc0a",
                                   "position": 64,
                                   "length": 8,
                                   "pitch": 69,
                               },
                               {
                                   "id": "note-236baf42-530b-4190-babf-bd8aa2276b57",
                                   "position": 72,
                                   "length": 16,
                                   "pitch": 71,
                               },
                               {
                                   "id": "note-aff5d867-41ed-4516-876f-3035dc0a164f",
                                   "position": 88,
                                   "length": 8,
                                   "pitch": 72,
                               },
                           ]
                   },
               ],
}

song1 = {
    # this song is an A minor harmonic scale, with notes starting at two semibreves and decreasing in length. This time there are two instruments, playing it in contrary motion (ie starting on the same note, one going up, one going down).
    "head":
        {
            "subDivisions": 16,
            "tempo": 120,
            "title": "Gangnam Style",
            "length": 16,
            "genre": "K-Pop",
            "tags": ["meme", "irritating"],
            "id": 1,
        },
    "tracks":
        [
            {
                "instrument": 16,  # drawbar organ
                "notes":
                    [
                        {
                            "id": "note-7d41083b-f0b2-4cba-bf25-d1089135a565",
                            "position": 0,
                            "length": 128,
                            "pitch": 69,
                        },
                        {
                            "id": "note-649122f4-e3b8-4fe6-84b5-cd7303460518",
                            "position": 128,
                            "length": 64,
                            "pitch": 71,
                        },
                        {
                            "id": "note-4ea0f2a1-d411-4ad9-ba4e-12c77c24e189",
                            "position": 192,
                            "length": 32,
                            "pitch": 72,
                        },
                        {
                            "id": "note-0c4c4ebc-ad2f-4ad0-bd0a-d73f5770399b",
                            "position": 224,
                            "length": 16,
                            "pitch": 74,
                        },
                        {
                            "id": "note-e1297763-6990-4878-89b6-9f43e88bc7d3",
                            "position": 240,
                            "length": 8,
                            "pitch": 76,
                        },
                        {
                            "id": "note-89a0d621-ad2f-4bb2-b13f-3addde099f52",
                            "position": 248,
                            "length": 4,
                            "pitch": 77,
                        },
                        {
                            "id": "note-3d98ca34-ba98-4cb9-9602-52ab3d8587b2",
                            "position": 252,
                            "length": 2,
                            "pitch": 80,
                        },
                        {
                            "id": "note-96be63e2-f918-46da-b2fe-9c11a56c28c5",
                            "position": 254,
                            "length": 1,
                            "pitch": 81,
                        },
                    ]
            },
            {
                "instrument": 40,  # violin
                "notes":
                    [
                        {
                            "id": "note-aa2e77f7-e0ae-42b2-91b4-b4cb797c6ead",
                            "position": 0,
                            "length": 128,
                            "pitch": 69,
                        },
                        {
                            "id": "note-6549669d-150c-4ad7-8b09-8767f266567d",
                            "position": 128,
                            "length": 64,
                            "pitch": 68,
                        },
                        {
                            "id": "note-387b1a8f-486d-4aa0-be1b-811382c46836",
                            "position": 192,
                            "length": 32,
                            "pitch": 65,
                        },
                        {
                            "id": "note-a47220eb-3a1a-4855-b680-4f0e88391467",
                            "position": 224,
                            "length": 16,
                            "pitch": 64,
                        },
                        {
                            "id": "note-2fdf9e04-1d9a-4073-8de6-ba4506e2167c",
                            "position": 240,
                            "length": 8,
                            "pitch": 62,
                        },
                        {
                            "id": "note-3766c3c7-e2d5-4a8f-8eb7-0d560ca958b9",
                            "position": 248,
                            "length": 4,
                            "pitch": 60,
                        },
                        {
                            "id": "note-e5e99f09-df50-4170-879a-86783f757657",
                            "position": 252,
                            "length": 2,
                            "pitch": 59,
                        },
                        {
                            "id": "note-21a2d827-6b16-44bf-8f86-30295011a703",
                            "position": 254,
                            "length": 1,
                            "pitch": 57,
                        },
                    ]
            },
        ],
}


class SongGetHandler(webapp2.RequestHandler):
    def get(self, songid):
        if not songid:
            self.abort(400)
        # This stuff will be handled by the database; this is just temporary to
        # test the web stuff
        if songid == "0":
            self.response.out.write(json.dumps(song0))
        elif songid == "1":
            self.response.out.write(json.dumps(song1))
        else:
            self.abort(404)


class NoteChangeHandler(webapp2.RequestHandler):
    def delete(self, songid):
        if not songid:
            return error.respond(400, "Invalid song ID in request URL")
        else:
            actionId = self.request.get("actionId")
            track = self.request.get("track")
            noteId = self.request.get("noteId")
            if actionId and track and noteId:
                datastore_request_object = {
                    'actionId': actionId,
                    'track': track,
                    'noteId': noteId
                }
                datastore.removeNote(songid, json.dumps(datastore_request_object))
                success_object = {
                    'status': 'true',
                }
                self.response.write(json.dumps(success_object))
                self.response.set_status(200)
                return
            else:
                return error.respond(400, 'Missing request parameter(s)')


application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/songs/get/<songid>', handler=SongGetHandler,
                                                        name='song-get-by-id'),
                                          webapp2.Route(r'/songs/<songid>/notes', handler=NoteChangeHandler,
                                                        name='notechanges'),
                                      ], debug=True)
					
