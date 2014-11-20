#!/usr/bin/env python
#
# This class generates Response objects carrying JSON payloads, logging as appropriate.
#

import webapp2

import json
import random
import logging


def respond(status, message):
    error_id = hex(random.getrandbits(64))
    logging.info('[' + str(error_id) + '] HTTP ' + str(status) + ' generated in response to: ' + message)
    error_object = {
        'status': status,
        'message': message,
        'errorId': error_id
    }
    response = webapp2.Response(json.dumps(error_object))
    response.set_status(status)
    return response