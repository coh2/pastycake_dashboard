'''main component of the dashboard'''
from flask import render_template, jsonify, request

import datetime
import sqlite3

# this imports is needed for routing and setup purposes
import pastycake_dashboard.crypto

from . import app


def _sqlite_conn(with_cursor=True):
    conn = sqlite3.connect(app.config.get('SQLITE_DB', 'urls.db'))
    if with_cursor:
        curs = conn.cursor()
        return (conn, curs)
    else:
        return conn


def _get_sqlite_matches(sqlitecon, since=None, startwith=None):
    curs = sqlitecon.cursor()
    newmax = int(curs.execute('SELECT max(id) FROM \
                                url_matches').fetchone()[0])
    curs.execute('''
        SELECT urls.url, match_expression, matched
        FROM url_matches JOIN urls JOIN matchers
        WHERE url_matches.url=urls.id AND url_matches.matcher=matchers.id
            AND viewed >= ? AND url_matches.id > ? and url_matches.id <= ?
            ORDER BY viewed DESC
    ''', (since or datetime.datetime(1, 1, 1),
          startwith or 0,
          newmax
         )
    )

    res = []
    for _ in curs.fetchall():
        res.append(dict(zip(('source_link', 'match_expression', 'match'), _)))
    return (newmax, res)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/get_latest')
def latest():
    # at most 20 seconds ago with an id > maxid
    timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=20)
    maxid = request.args.get('id', -1, type=int)

    conn = _sqlite_conn(False)
    (maxid, matches) = _get_sqlite_matches(conn, since=timestamp, startwith=maxid)
    conn.close()

    dom = render_template('ajax_latest.html', matches=matches)
    data = {'id': maxid, 'dom': dom}

    res = jsonify(data)
    return res


@app.route('/keywords', methods=['GET', 'POST'])
def keywords():
    return render_template('kw_form.html', keywords={})
