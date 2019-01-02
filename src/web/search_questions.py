
from flask import render_template, request
from .utils import read_int_from_form
from . import app
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

@app.route('/bankdomain/search_questions', methods=['GET'])
@app.route('/search_questions', methods=['GET'])
def search_questions():
    _ = app.application
    random_questions = []
    for i in range(5):
        random_questions.append(_.mongo_repository.retrieve_random_question())
    return render_template('search_questions.html', random_questions=random_questions)

@app.route('/bankdomain/search_questions_submit', methods=['POST'])
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
                random_questions = []
                for i in range(5):
                    random_questions.append(_.mongo_repository.retrieve_random_question())
                return render_template('search_questions.html',messages = messages, random_questions=random_questions)
            else:
                page_id = read_int_from_form(form, 'page_id', "0")
                return do_search(_, page_id, question)


def do_search(_, page_id, question):
    logging.info("Processing {}".format(question))
    answers = _.query_executor.retrieve_answers(question, threshold=0.78, topn=20)
    scores, token_map, tokens_not_found = answers["scores"], answers["token_map"], answers[
        "tokens_not_found"]
    docs = _.query_executor.retrieve_documents(scores, page_id)
    token_list = [{"token": key, "rel_tokens": ", ".join([v[0] + " (" + str(round(v[1], 2)) + ")" for v in values])} for
                  key, values in token_map.items()]
    return render_template('search_questions.html', docs=docs, page_id=page_id, question=question,
                           token_list=token_list, tokens_not_found=tokens_not_found)


@app.route('/bankdomain/random_questions_submit', methods=['POST'])
@app.route('/random_questions_submit', methods=['POST'])
def random_question_submit():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        question = _.mongo_repository.retrieve_random_question()
        return do_search(_, 0, question)

