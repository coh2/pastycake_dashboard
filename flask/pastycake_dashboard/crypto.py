from __future__ import division

from datetime import timedelta

from . import app

import hashlib
import hmac
import math
import os

import flask

import db_sqlite as db


def _new_token(strength=128):
    '''create a general-purpose token of the required strength'''
    length = int(math.ceil(strength / 7.995)) * 2  # birthday resistance / hex
    return hashlib.sha512(os.urandom(length)).hexdigest()[:length]


def _const_time_compare(val1, val2):
    '''compare if a == b in a _mostly_ time constant manner

    return True if a == b, False otherwise.
    '''
    assert type(val1) == type(val2)
    if len(val1) != len(val2):
        return False
    res = 0
    for i in range(len(val1)):
        res |= ord(val1[i]) ^ ord(val2[i])
    return not bool(res)


@app.before_request
def csrf_protect():
    '''check if a proper csrf token has been supplied with any POST request'''
    if flask.request.method == 'POST':
        username = flask.session.get('username')
        userid = db.get_userid_for_username(username)
        field = '_csrf_update'
        token = flask.session.pop(field, '')
        h = hmac.new(app.config['SECRET_KEY'], digestmod=hashlib.sha256)
        h.update(token)
        if not token or not _const_time_compare(h.hexdigest(),
                                                flask.request.form.get(field)):
            app.logger.info('invalid CSRF token for user %s (id %s) \
                            logged in from ip %s' % (
                username, userid, flask.request.remote_addr))
            flask.abort(403)


def new_csrf_token(field):
    '''create a new CSRF token.

    make the session-stored piece different from the field one by
    applying a hash/hmac onto it in combination with the secret key.

    '''
    temp = _new_token()
    h = hmac.new(app.config['SECRET_KEY'], digestmod=hashlib.sha256)
    h.update(temp)
    flask.session[field] = temp
    return h.hexdigest()


app.jinja_env.globals['csrf_token'] = new_csrf_token
