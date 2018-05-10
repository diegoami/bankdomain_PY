
from flask import render_template, request


from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@app.route('/bankdomain/show_words', methods=['GET'])
@app.route('/show_words', methods=['GET'])
def show_words():

    _ = app.application
    words = _.model_facade.doc2vecFacade.retrieve_words()
    wps = []
    for word, count in words:
        if (count >= 8):
            sim_w = _.model_facade.doc2vecFacade.pull_scores_word(word, threshold=0.8, topn=20)
            forms = _.language_facade.retrieve_forms_for_lemma(word)
            wps.append( { "word" : word, "count" : count,
                          "forms" : ", ".join([f for f in forms ]),
                          "simw" :  ", ".join([v[0]+" ("+str(round(v[1],2)) +")" for v in sim_w ])

                         })


    return render_template('show_words.html', wps=wps)