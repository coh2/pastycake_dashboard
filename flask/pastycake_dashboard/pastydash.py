'''main component of the dashboard'''
from flask import render_template, jsonify, request, abort

from . import app

import crypto
import datetime


backend = None


def _load_backend():
    #TODO
    return True


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/get_latest')
def latest():
    if not backend:
        _load_backend() or abort(503)

    # at most 20 seconds ago with an id > maxid
    timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=20)
    maxid = request.args.get('id', -1, type=int)
    (maxid, matches) = backend.get_matches(since=timestamp, maxid=maxid)

    dom = render_template('ajax_latest.html', matches=matches)
    data = {'id': maxid, 'dom': dom}

    return jsonify(data)
