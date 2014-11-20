#!/usr/bin/env python
#
# This class generates Response objects carrying JSON payloads, logging as appropriate.
#

import webapp2

import json
import random
import logging


def respond(status, message):
    response = webapp2.Response
    error_id = hex(random.getrandbits(64))
    logging.info('[' + error_id + '] HTTP ' + status + ' generated in response to: ' + message)
    error_object = {
        'status': status,
        'message': message,
        'errorId': error_id
    }
    response.write(json.dumps(error_object))
    response.set_status(400)
    return response