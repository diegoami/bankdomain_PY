
from flask import render_template, request


from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@app.route('/bankdomain/show_words', methods=['GET'])
@app.route('/show_words', methods=['GET'])
def show_words():
    messages = []
    _ = app.application
    if _.wps:
        return render_template('show_words.html', wps=_.wps)
    else:
        messages.append('Words not loaded yet, come back later')
        return render_template('show_words.html', messages=messages)
