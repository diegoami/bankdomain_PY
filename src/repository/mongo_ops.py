
from pymongo import MongoClient
import os
import sys
import bson
import logging
import traceback

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

    def import_questions(self, data_dirs, append=False):
        new_documents = self.copy_into_qa_documents(data_dirs, append=append)
        self.split_qa_documents_into_questions(new_documents, append=append)

    def copy_into_qa_documents(self, data_dirs, append=False):
        logging.info("Importing all documents")
        qa_documents_coll = self.bankdomain_db.qa_documents
        if not append:
            qa_documents_coll.remove()
        new_documents = []
        errors = 0
        for data_dir in data_dirs:
            logging.info("Importing documents from {}".format(data_dir))

            for root, subdirs, files in os.walk(data_dir):
                for file in files:
                    full_file = os.path.join(root,file)
                    full_file_db = full_file.encode('utf-8', 'surrogateescape').decode('ISO-8859-1')
                    logging.info("Processing file {}".format(full_file))
                    try:
                        if not append or not qa_documents_coll.count({'full_file': full_file_db}):
                            logging.info("Inserting document {}".format(full_file_db))
                            with open(full_file, 'r', encoding="utf-8") as f:
                                content = f.readlines()

                                qa_documents_coll.save(
                                    {'full_file': full_file_db, 'content': content}
                                )
                                new_documents.append(full_file)
                        else:
                            logging.info("Skpping document {}".format(full_file_db))

                    except:
                        errors += 1
                        traceback.print_exc()
                        logging.error("Could not read file {}".format(full_file))

                    if errors > 10:
                        logging.fatal("Too many files unaccessible")
                        sys.exit(1)
            logging.info("Imported files from {}".format(data_dir))

        logging.info("Finished Importing all documents")
        return new_documents

    def split_qa_documents_into_questions(self, new_documents, append):
        logging.info("Splitting documents into questions....")
        qa_documents_coll = self.bankdomain_db.qa_documents
        qa_questions_coll = self.bankdomain_db.qa_questions
        if not append:
            qa_questions_coll.remove()
            index = 0
        else:
            index = qa_questions_coll.count()
        qa_documents_in_db = qa_documents_coll.find()
        answer, question = "", ""

        for i, el in enumerate(qa_documents_in_db):
            full_file = el["full_file"]
            if full_file in new_documents:
                logging.info("Processing document {}...".format(full_file))
                content = el["content"]
                el["processed"] = True
                state = 0

                for line_l in content:
                    line = line_l.strip()
                    if '###' in line:
                        state = 0
                        if len(question) > 0 and len(answer) > 0:
                            qa_questions_coll.insert_one({"question": question, "answer" : answer, "full_file": el["full_file"], "index" :  bson.Int64(index)})
                            index += 1
                            answer, question = "", ""
                    elif len(line) == 0:
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
            else:
                logging.info("Skipping document {}...".format(full_file))

        logging.info("Finished splitting documents into questions....")

    def iterate_questions (self, collection, separator=False, print_number=False, lowercase = False, only_question=False):
        questions_db = collection.find().sort( u"index", 1  )
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
        with open(output_dir + '/questions.txt', 'w', encoding="utf-8") as f:
            f.writelines(self.iterate_questions(collection=self.questions, separator=True, print_number=True), )

        with open(output_dir + '/preprocessed_questions.txt', 'w', encoding="utf-8") as f:
            f.writelines(
                self.iterate_questions(collection=self.preprocessed_questions, separator=True,  print_number=True))

        with open(output_dir + '/processed_questions.txt', 'w', encoding="utf-8") as f:
            f.writelines(
                self.iterate_questions(collection=self.processed_questions, separator=True,  print_number=True))

    def process_questions(self, source_collection, target_collection, processor, append=False):
        logging.info("Starting transfer from collection {} to collection {}".format(source_collection, target_collection))
        if append:
            start_index = target_collection.count()
            condition = { "$gte" : start_index }
            source_records = source_collection.find( {"index": condition }).sort(u"index", 1)

        else:
            source_records = source_collection.find().sort(u"index", 1)
            start_index = 0
            target_collection.remove()
        all_texts = []
        for idx, el in enumerate(source_records) :
            if (idx % 100) == 0:
                logging.info("process_questions: Processed {} rows".format(idx))
            to_write = {"question": processor(el["question"]) , "answer":processor(el["answer"]), "index": el["index"] }
            target_collection.insert_one(to_write)
            all_texts.append(to_write["question"]+"\n"+to_write["answer"])

        logging.info("Finished transfer from collection {} to collection {}".format(source_collection, target_collection))

    def load_all_documents(self):
        self.preprocessed_questions_no_answer = [question for question in self.iterate_questions(collection=self.preprocessed_questions, only_question=True)]
        self.preprocessed_questions_with_answer = [question for question in self.iterate_questions(collection=self.preprocessed_questions, only_question=False)]
        self.num_questions = len(self.preprocessed_questions_no_answer)
        self.all_preprocessed_questions = self.preprocessed_questions_no_answer + self.preprocessed_questions_with_answer
        self.questions_no_answer = [question.split() for question in self.iterate_questions(collection=self.processed_questions, lowercase=True, only_question=True)]
        self.questions_with_answer = [question.split() for question in self.iterate_questions(collection=self.processed_questions, lowercase=True, only_question=False)]
        self.all_questions = self.questions_no_answer + self.questions_with_answer


    def get_all_questions(self):
        return self.all_questions

    def get_preprocessed_question(self, index):
        if (index >= len(self.preprocessed_questions_with_answer)):
            index -= len(self.preprocessed_questions_with_answer)
        return self.preprocessed_questions_with_answer[index]

    def retrieve_random_question(self):
        rand_index = randint(0, self.num_questions)
        return self.all_preprocessed_questions[rand_index]
