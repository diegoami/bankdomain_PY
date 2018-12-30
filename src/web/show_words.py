
from flask import render_template, request


from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@app.route('/bankdomain/show_words', methods=['GET'], defaults={'min_count': 8})
@app.route('/bankdomain/show_words/<int:min_count>', methods=['GET'])
@app.route('/show_words', methods=['GET'], defaults={'min_count': 8})
@app.route('/show_words/<int:min_count>', methods=['GET'])
def show_words(min_count):
    messages = []
    _ = app.application
    if _.wps and _.wps_count == min_count:
        return render_template('show_words.html', wps=_.wps)
    else:
        _.start_load_words(min_count)
        messages.append('Words not loaded yet, come back later')
        return render_template('show_words.html', messages=messages)
