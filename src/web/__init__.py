from flask import Flask
from flask import redirect, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/bankdomain/')
def home():
    return redirect(url_for('search_questions'))

import web.search_questions
import web.show_clusters
import web.show_words
import web.show_grams
import web.sign_in