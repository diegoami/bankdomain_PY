from flask import Flask
from flask import redirect, url_for


app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('search_questions'))

import web.search_questions