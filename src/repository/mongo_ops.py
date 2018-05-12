
from pymongo import MongoClient
import os
import bson
import logging
import pandas
from random import randint
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
        logging.info("Importing all documents")
        qa_documents_coll = self.bankdomain_db.qa_documents
        qa_documents_coll.remove()

        for root, subdirs, files in os.walk(data_dir):
            for file in files:
                full_file = root + "/" + file
                try:
                    with open(full_file, 'r') as f:
                        content = f.readlines()
                        qa_documents_coll.save({'full_file': full_file, 'content': content})
                except:
                    logging.error("Could not read file {}".format(full_file))
        logging.info("Finished Importing all documents")

    def split_qa_documents_into_questions(self):
        logging.info("Splitting documents into questions....")
        qa_documents_coll = self.bankdomain_db.qa_documents
        qa_questions_coll = self.bankdomain_db.qa_questions
        qa_questions_coll.remove()
        qa_documents_in_db = qa_documents_coll.find()
        answer, question = "", ""
        index = 0
        for  el in qa_documents_in_db:
            content = el["content"]
            el["processed"] = True
            state = 0

            for line in content:
                if '###' in line:
                    state = 0
                    if len(question) > 0 and len(answer) > 0:
                        qa_questions_coll.insert_one({"question": question, "answer" : answer, "full_file": el["full_file"], "index" :  bson.Int64(index)})
                        index += 1
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
                qa_questions_coll.insert_one({"question": question, "answer": answer, "full_file": el["full_file"],  "index" :bson.Int64(index)})
                index += 1
                answer, question = "", ""
            qa_documents_coll.save(el)
        logging.info("Finished splitting documents into questions....")

    def iterate_questions (self, collection, separator=False, print_number=False, lowercase = False, only_question=False):
        questions_db = collection.find()
        for index, el in enumerate(questions_db):

            if (separator):
                if (print_number):
                    yield "======== " +str(el["index"]) +" =====================================\n"
                else:
                    yield "=======================================================\n"
            if (lowercase):
                yield (el["question"].lower() + (("\n"+ el["answer"].lower() ) if not only_question else "") +"\n")
            else:
                yield (el["question"] + (("\n"+ el["answer"] )if not only_question else "")  + "\n")

    def print_all_files(self, output_dir):
        with open(output_dir + '/questions.txt', 'w') as f:
            f.writelines(self.iterate_questions(collection=self.questions, separator=True, print_number=True))

        with open(output_dir + '/preprocessed_questions.txt', 'w') as f:
            f.writelines(
                self.iterate_questions(collection=self.preprocessed_questions, separator=True,  print_number=True))

        with open(output_dir + '/processed_questions.txt', 'w') as f:
            f.writelines(
                self.iterate_questions(collection=self.processed_questions, separator=True,  print_number=True))

    def process_questions(self, source_collection, target_collection, processor):
        logging.info("Starting transfer from collection {} to collection {}".format(source_collection, target_collection))
        source_records = source_collection.find().sort( u"index", 1  )
        target_collection.remove()
        all_texts = []
        for idx, el in enumerate(source_records) :
            if (idx % 100) == 0:
                logging.debug("Processed {} rows".format(idx))
            to_write = {"question": processor(el["question"]) , "answer":processor(el["answer"]), "index": el["index"] }
            target_collection.insert_one(to_write)
            all_texts.append(to_write["question"]+"\n"+to_write["answer"])

        logging.info("Finished transfer from collection {} to collection {}".format(source_collection, target_collection))

    def load_all_documents(self):
        preprocessed_questions_no_answer = [question for question in self.iterate_questions(collection=self.preprocessed_questions, only_question=True)]
        preprocessed_questions_with_aswer = [question for question in self.iterate_questions(collection=self.preprocessed_questions, only_question=False)]
        self.num_questions = len(preprocessed_questions_no_answer)
        self.all_preprocessed_questions = preprocessed_questions_no_answer + preprocessed_questions_with_aswer
        processed_splitted_questions_no_answer = [question.split() for question in self.iterate_questions(collection=self.processed_questions, lowercase=True, only_question=True)]
        processed_splitted_questions_with_answer = [question.split() for question in self.iterate_questions(collection=self.processed_questions, lowercase=True, only_question=False)]
        self.all_processed_splitted_questions = processed_splitted_questions_no_answer+ processed_splitted_questions_with_answer
        self.panda = pandas.DataFrame(self.all_preprocessed_questions)

    def get_preprocessed_question(self, index):
        if (index < self.num_questions):
            index += self.num_questions
        return self.all_preprocessed_questions[index]

    def retrieve_random_question(self):
        rand_index = randint(0, self.num_questions)
        return self.all_preprocessed_questions[rand_index]
