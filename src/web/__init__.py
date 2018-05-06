from flask import Flask
from flask import redirect, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/banking/')
def home():
    return redirect(url_for('search_questions'))

import web.search_questions
import web.show_clusters