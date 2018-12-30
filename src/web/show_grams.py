
from flask import render_template, request


from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@app.route('/bankdomain/show_grams', methods=['GET'])
@app.route('/show_grams', methods=['GET'])
def show_grams():
    messages = []
    _ = app.application
    grams = _.load_grams()
    return render_template('show_grams.html', grams=grams, messages=messages)