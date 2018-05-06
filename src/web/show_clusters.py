
from flask import render_template, request
from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


@app.route('/show_clusters', methods=['GET'])
def show_clusters():

    return  render_template('show_clusters.html')

@app.route('/show_clusters_submit', methods=['POST'])
def show_clusters_submit():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        messages = []
        if form:

            num_clusters = read_int_from_form(form, 'num_clusters', "0")
            if (num_clusters > 0):
                cluster_map = _.model_facade.retrieve_clusters(num_clusters=num_clusters  )
                clusters = sorted([{"index" : key, "words" :  ", ".join(sorted(values))}
                            for key, values in cluster_map.items() ], key= lambda x: x["index"])
                return render_template('show_clusters.html', clusters=clusters, num_clusters=num_clusters)
            else :
                return render_template('show_clusters.html')
