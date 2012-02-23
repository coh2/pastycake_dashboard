'''Run the dashboard.'''

from __future__ import division

import math
import os
import sys

from pastycake_dashboard.pastydash import app


def _setup_security(appobj):
    '''
    setup required security features.
    '''
    # adjusted for imperfect entropy based on tests under linux
    appobj.secret_key = os.urandom(int(math.ceil(256 / 7.991)))

    host = app.config.get('HOST', '127.0.0.1')

    if (not host.startswith('127.') or
        host not in ('::1', '0:0:0:0:0:0:0:1')) and appobj.debug:
        raise RuntimeError('public facing + debug enabled = you WILL get \
                            owned')


if len(sys.argv) > 1:
    app.config.from_pyfile(sys.argv[1])

for k, v in app.config.items():
    print k, v
_setup_security(app)

app.run(host=app.config.get('HOST', '127.0.0.1'))
