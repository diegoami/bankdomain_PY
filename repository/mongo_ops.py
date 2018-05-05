
from pymongo import MongoClient
import os

class MongoRepository:
    def __init__(self, mongo_connection):
        self.mongo_connection = mongo_connection
        self.mongo_client = MongoClient(self.mongo_connection)
        self.bankdomain_db = self.mongo_client.bankdomain
        self.documents = self.bankdomain_db.qa_documents
        self.questions = self.bankdomain_db.qa_questions
        self.preprocessed_questions = self.bankdomain_db.proc_questions
        self.processed_questions = self.bankdomain_db.mod_questions

    def import_questions(self, data_dir):
        self.copy_into_qa_documents(data_dir)
        self.split_qa_documents_into_questions()

    def copy_into_qa_documents(self, data_dir):
        qa_documents_coll = self.bankdomain_db.qa_documents
        qa_documents_coll.remove()

        for root, subdirs, files in os.walk(data_dir):
            for file in files:
                full_file = root + "/" + file
                with open(full_file, 'r') as f:
                    content = f.readlines()

                    qa_documents_coll.save({'full_file': full_file, 'content': content})


    def split_qa_documents_into_questions(self):
        qa_documents_coll = self.bankdomain_db.qa_documents
        qa_questions_coll = self.bankdomain_db.qa_questions
        qa_questions_coll.remove()
        qa_documents_in_db = qa_documents_coll.find()
        answer, question = "", ""
        for el in qa_documents_in_db:
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

    def iterate_questions (self, collection, separator=False):
        questions_db = collection.find()
        for index, el in enumerate(questions_db):
            yield (el["question"] + "\n"+ el["answer"]+"\n")
            if (separator):
                yield "====================================================\n"

    def process_questions(self, source_collection, target_collection, processor):
        source_records = source_collection.find()
        target_collection.remove()
        all_texts = []
        for el in source_records :
            to_write = {"question": processor(el["question"]) , "answer":processor(el["answer"]), "ref_qa": el["_id"] }
            target_collection.insert_one(to_write)
            all_texts.append(to_write["question"]+"\n"+to_write["answer"])
        return all_texts
