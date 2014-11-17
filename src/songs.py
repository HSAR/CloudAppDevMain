#!/usr/bin/env python

import os
import datetime

import webapp2
import jinja2

import json

from google.appengine.api import users
from google.appengine.api import channel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

song0 = { # this song is just a C major scale, but with notes alternating between crotchets and quavers.
        "head":
        {
            "subDivisions": 16,
            "tempo": 120,
            "title": "Zubion",
            "length": 6, # what the hell is this measured in? Beats? I'm guessing beats.
            "genre": "French",
            "tags": [ "ou", "est", "la", "gare"],
            "id": 0,
        },
        "tracks":
        [
            {
                "instrument": 0, # acoustic grand piano
                "notes":
                [
                    {
                        "id": "24e7f3c5-d2f0-4e40-aae0-3e687d901bde",
                        "pos": 0,
                        "length": 16,
                        "note": 60,
                    },
                    {
                        "id": "78a06d95-97e1-44cd-9175-e4617a1a206a",
                        "pos": 16,
                        "length": 8,
                        "note": 62,
                    },
                    {
                        "id": "635fbf94-a45a-4b90-940c-a5cf245ccdac",
                        "pos": 24,
                        "length": 16,
                        "note": 64,
                    },
                    {
                        "id": "f36f02d5-6da8-4459-9c01-014efcffe56e",
                        "pos": 40,
                        "length": 8,
                        "note": 65,
                    },
                    {
                        "id": "9ec8b033-0f4b-4688-b6f1-42782964dcaf",
                        "pos": 48,
                        "length": 16,
                        "note": 67,
                    },
                    {
                        "id": "4a3320b5-0c60-4766-9d09-8a272e0afc0a",
                        "pos": 64,
                        "length": 8,
                        "note": 69,
                    },
                    {
                        "id": "236baf42-530b-4190-babf-bd8aa2276b57",
                        "pos": 72,
                        "length": 16,
                        "note": 71,
                    },
                    {
                        "id": "aff5d867-41ed-4516-876f-3035dc0a164f",
                        "pos": 88,
                        "length": 8,
                        "note": 72,
                    },
                ]
            },
        ],
}


song1 = { # this song is an A minor harmonic scale, with notes starting at two semibreves and decreasing in length. This time there are two instruments, playing it in contrary motion (ie starting on the same note, one going up, one going down).
        "head":
        {
            "subDivisions": 16,
            "tempo": 120,
            "title": "Gangnam Style",
            "length": 16,
            "genre": "K-Pop",
            "tags": [ "meme", "irritating"],
            "id": 1,
        },
        "tracks":
        [
            {
                "instrument": 16, # drawbar organ
                "notes":
                [
                    {
                        "id": "7d41083b-f0b2-4cba-bf25-d1089135a565",
                        "pos": 0,
                        "length": 128,
                        "note": 69,
                    },
                    {
                        "id": "649122f4-e3b8-4fe6-84b5-cd7303460518",
                        "pos": 128,
                        "length": 64,
                        "note": 71,
                    },
                    {
                        "id": "4ea0f2a1-d411-4ad9-ba4e-12c77c24e189",
                        "pos": 192,
                        "length": 32,
                        "note": 72,
                    },
                    {
                        "id": "0c4c4ebc-ad2f-4ad0-bd0a-d73f5770399b",
                        "pos": 224,
                        "length": 16,
                        "note": 74,
                    },
                    {
                        "id": "e1297763-6990-4878-89b6-9f43e88bc7d3",
                        "pos": 240,
                        "length": 8,
                        "note": 76,
                    },
                    {
                        "id": "89a0d621-ad2f-4bb2-b13f-3addde099f52",
                        "pos": 248,
                        "length": 4,
                        "note": 77,
                    },
                    {
                        "id": "3d98ca34-ba98-4cb9-9602-52ab3d8587b2",
                        "pos": 252,
                        "length": 2,
                        "note": 80,
                    },
                    {
                        "id": "96be63e2-f918-46da-b2fe-9c11a56c28c5",
                        "pos": 254,
                        "length": 1,
                        "note": 81,
                    },
                ]
            },
            {
                "instrument": 40, # violin
                "notes":
                [
                    {
                        "id": "aa2e77f7-e0ae-42b2-91b4-b4cb797c6ead",
                        "pos": 0,
                        "length": 128,
                        "note": 69,
                    },
                    {
                        "id": "6549669d-150c-4ad7-8b09-8767f266567d",
                        "pos": 128,
                        "length": 64,
                        "note": 68,
                    },
                    {
                        "id": "387b1a8f-486d-4aa0-be1b-811382c46836",
                        "pos": 192,
                        "length": 32,
                        "note": 65,
                    },
                    {
                        "id": "a47220eb-3a1a-4855-b680-4f0e88391467",
                        "pos": 224,
                        "length": 16,
                        "note": 64,
                    },
                    {
                        "id": "2fdf9e04-1d9a-4073-8de6-ba4506e2167c",
                        "pos": 240,
                        "length": 8,
                        "note": 62,
                    },
                    {
                        "id": "3766c3c7-e2d5-4a8f-8eb7-0d560ca958b9",
                        "pos": 248,
                        "length": 4,
                        "note": 60,
                    },
                    {
                        "id": "e5e99f09-df50-4170-879a-86783f757657",
                        "pos": 252,
                        "length": 2,
                        "note": 59,
                    },
                    {
                        "id": "21a2d827-6b16-44bf-8f86-30295011a703",
                        "pos": 254,
                        "length": 1,
                        "note": 57,
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

		

		
application = webapp2.WSGIApplication([
					webapp2.Route(r'/songs/get/<songid>', handler=SongGetHandler, name='song-get-by-id'),
				      ], debug=True)
