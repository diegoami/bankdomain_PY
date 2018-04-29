
from pymongo import MongoClient
import os

def copy_into_qa_documents(data_dir, mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_documents_coll = bankdomain_db.qa_documents
    qa_documents_in_db = qa_documents_coll.find()
    qa_documents_list = {}
    for el in qa_documents_in_db:
        qa_documents_list["full_file"] = {"full_file": el["full_file"], "content": el["content"]}
    for root, subdirs, files in os.walk(data_dir):
        for file in files:
            full_file = root + "/" + file
            with open(full_file, 'r') as f:
                content = f.readlines()
                if full_file in qa_documents_list:
                    key, value = {'full_file': full_file}, {'content': content}
                    qa_documents_coll.update_one(key, {'$set': value})
                else:
                    qa_documents_coll.insert_one({'full_file': full_file, 'content': content})


def print_all_questions(mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_questions_coll = bankdomain_db.qa_questions


    qa_questions_in_db = qa_questions_coll.find()
    for el in qa_questions_in_db:
        print("Q: {} \nA: {}".format(el["question"], el["answer"]))


def iterate_questions_in_mongo(mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_questions_coll = bankdomain_db.qa_questions

    qa_questions_in_db = qa_questions_coll.find()
    for el in qa_questions_in_db:
        yield (el["question"] + "\n"+ el["answer"])


def split_qa_documents_into_questions(mongo_connection):
    mongo_client = MongoClient(mongo_connection)
    bankdomain_db = mongo_client.bankdomain
    qa_documents_coll = bankdomain_db.qa_documents
    qa_questions_coll = bankdomain_db.qa_questions

    qa_documents_in_db = qa_documents_coll.find()
    answer, question = "", ""
    for el in qa_documents_in_db:
        if "processed" not in el:
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
        to_write = {"question": processor(el["question"], **kwargs) , "answer":processor(el["answer"], **kwargs)}
        proc_questions_coll.insert_one(to_write)
        all_texts.append(to_write["question"]+"\n"+to_write["answer"])
    return all_texts