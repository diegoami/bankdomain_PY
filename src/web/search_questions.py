
from flask import render_template, request
from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


@app.route('/search_questions', methods=['GET'])
def search_questions():

    return render_template('search_questions.html')

@app.route('/search_questions_submit', methods=['POST'])
def search_questions_submit():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        messages = []
        if form:

            question = form['question']
            if not question or len(question.strip()) < 3:
                messages.append('Please enter a question')
                return render_template('search_questions.html',messages = messages)
            else:
                page_id = read_int_from_form(form, 'page_id', "0")
                logging.info("Processing {}".format(question))
                scores_tfidf, token_map = _.query_executor.retrieve_answers(question )
                docs_tfidf = _.query_executor.retrieve_documents(scores_tfidf, page_id)
                token_list = [ {"token" : key, "rel_tokens": ", ".join([v[0]+" ("+str(round(v[1],2)) +")" for v in values])} for key, values in token_map.items()]

                return render_template('search_questions.html', docs_tfidf=docs_tfidf, page_id = page_id, question=question, token_list = token_list)

