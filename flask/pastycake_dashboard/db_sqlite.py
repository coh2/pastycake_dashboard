from pastycake_dashboard import app

import datetime
import sqlite3


_DB_TABLES = '''
BEGIN;
create table users (
    id integer unique primary key autoincrement,
    name varchar(64) unique not null,
    password string unique not null,
    email string unique not null,
    pending_approval boolean default true
);

create table user_tokens (
    user_id references users(id),
    token string unique,
    timestamp integer default CURRENT_TIMESTAMP,
    last_action integer default CURRENT_TIMESTAMP
);

COMMIT;
'''


def connect_db(connection_only=False):
    conn = sqlite3.connect(app.config['DATABASE'])
    if connection_only:
        return conn
    else:
        return (conn, conn.cursor())


def get_userid_for_username(username):
    '''find the id for a given username'''
    if not username:
        return None
    (conn, curs) = connect_db()
    res = curs.execute('''
        SELECT id FROM users
        WHERE name=?
        LIMIT 1''', (username,)
    ).fetchone()
    return int(res[0]) if res else None


def sqlite3_to_datetime(datestr):
    '''convert sqlite3 datetime to datetime timestamp'''
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
