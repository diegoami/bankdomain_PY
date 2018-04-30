
from pymongo import MongoClient
import os

def copy_into_qa_documents(data_dir, mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_documents_coll = bankdomain_db.qa_documents
    qa_documents_coll.remove()
    #qa_documents_in_db = qa_documents_coll.find()
   # qa_documents_list = {}
  #  for el in qa_documents_in_db:
  #      qa_documents_list["full_file"] = {"full_file": el["full_file"], "content": el["content"]}
    for root, subdirs, files in os.walk(data_dir):
        for file in files:
            full_file = root + "/" + file
            with open(full_file, 'r') as f:
                content = f.readlines()

                qa_documents_coll.save({'full_file': full_file, 'content': content})


def print_all_questions(mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_questions_coll = bankdomain_db.qa_questions


    qa_questions_in_db = qa_questions_coll.find()
    for el in qa_questions_in_db:
        print("Q: {} \nA: {}".format(el["question"], el["answer"]))


def iterate_questions_in_mongo(mongo_connection,separator=False):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_questions_coll = bankdomain_db.qa_questions
    qa_questions_in_db = qa_questions_coll.find()
    for el in qa_questions_in_db:
        yield (el["question"] + "\n"+ el["answer"]+"\n")
        if (separator):
            yield "====================================================\n"

def iterate_proc_questions_in_mongo(mongo_connection,separator=False):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    proc_questions_coll = bankdomain_db.proc_questions
    proc_questions_in_db = proc_questions_coll .find()
    for el in proc_questions_in_db:
        yield (el["question"] + "\n"+ el["answer"]+"\n")
        if (separator):
            yield "====================================================\n"


def split_qa_documents_into_questions(mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_documents_coll = bankdomain_db.qa_documents
    qa_questions_coll = bankdomain_db.qa_questions
    qa_questions_coll.remove()
    qa_documents_in_db = qa_documents_coll.find()
    answer, question = "", ""
    for el in qa_documents_in_db:
##        if "processed" not in el:
            content = el["content"]
            el["processed"] = True
            state = 0

            for line in content:
                if '###' in line:
                    state = 0
                    if len(question) > 0 and len(answer) > 0:
                        qa_questions_coll.insert_one({"question": question, "answer" : answer, "full_file": el["full_file"]})
                        answer, question = "", ""
                elif len(line.strip()) == 0:
                    continue
                elif state == 0:
                    question = line
                    state = 1
                else:
                    if len(answer) > 0:
                        answer = answer + "\n"
                    answer = answer + line


            if len(question) > 0 and len(answer) > 0:
                qa_questions_coll.insert_one({"question": question, "answer": answer, "full_file": el["full_file"]})
                answer, question = "", ""
            qa_documents_coll.save(el)


def process_questions(mongo_connection, processor, **kwargs):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_questions_coll = bankdomain_db.qa_questions
    qa_questions_in_db = qa_questions_coll.find()
    proc_questions_coll = bankdomain_db.proc_questions
    proc_questions_coll.remove()
    all_texts = []
    for el in qa_questions_in_db :
        to_write = {"question": processor(el["question"], **kwargs) , "answer":processor(el["answer"], **kwargs), "ref_qa": el["_id"] }
        proc_questions_coll.insert_one(to_write)
        all_texts.append(to_write["question"]+"\n"+to_write["answer"])
    return all_texts


def question_for_model(mongo_connection, processor, nlp):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    proc_questions_coll = bankdomain_db.proc_questions
    proc_questions_in_db = proc_questions_coll.find()
    mod_questions_coll = bankdomain_db.mod_questions_coll
    mod_questions_coll.remove()
    all_texts = []
    for el in proc_questions_in_db:
        to_write = {"question": processor(el["question"],nlp) , "answer":processor(el["answer"], nlp), "ref_proc": el["_id"],  "ref_qa": el["ref_qa"]}
        mod_questions_coll.insert_one(to_write)
        all_texts.append(to_write["question"]+"\n"+to_write["answer"])
    return all_texts

