'''Run the dashboard.'''

from __future__ import division

import math
import os
import os.path
import sys

from pastycake_dashboard.pastydash import app


def _setup_security(appobj):
    '''
    setup required security features.
    '''
    # adjusted for imperfect entropy based on tests under linux
    appobj.secret_key = os.urandom(int(math.ceil(256 / 7.995)))

    host = app.config.get('HOST', '127.0.0.1')

    if (not host.startswith('127.') and
        host not in ('::1', '0:0:0:0:0:0:0:1')) and appobj.debug:
        raise RuntimeError('public facing + debug enabled = you WILL get \
                            owned')


def main():
    '''main routine to setup required stuff and run the app'''
    if len(sys.argv) > 1:
        conffile = sys.argv[1]

        if not os.path.isabs(conffile):
            conffile = os.path.abspath(conffile)

        app.config.from_pyfile(conffile)

    _setup_security(app)
    app.run(host=app.config.get('HOST', '127.0.0.1'))


main()
