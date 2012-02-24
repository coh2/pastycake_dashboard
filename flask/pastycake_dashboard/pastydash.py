'''main component of the dashboard'''
from flask import render_template

from . import app

import crypto


@app.route('/')
def main():
    return render_template('index.html', data={})
