
See it live at http://www.faqportal.de

## SCRIPTS

* faqs_from_yml.py: to generate FAQs from a crawl definition file
* create_model.py: to create database and model
* boot_web.py: to start the web application


## SET UP DATABASE

Make sure you set up an instance of mongo. The database will be called bankdomain

The documents are contained in the github repository: _https://github.com/diegoami/bankdomain.git_

Make sure that the documents directory links to   _/media/diego/QData/bankdomain/docs/qa_documents_ .

~~~~
git clone https://github.com/diegoami/bankdomain.git
ln -s $(pwd)/bankdomain/qa_documents /media/diego/QData/bankdomain/docs/qa_documents 
~~~~

and then execute

~~~~
cd src && python create_model.py
~~~~

## START WEB APPLICATION

~~~~
cd src && python boot_web.py

OR

~~~~

## DOCKER

~~~~
mkdir -p ~/model
mkdir -p ~/db

~~~~

~~~~

docker build -f docker/mongo/Dockerfile  --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/mongo .

docker build -f docker/portal/Dockerfile --build-arg SECRET_KEY=... --build-arg  --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/model .

docker network create -d bridge mybridge

docker run -d --network=mybridge -p 27017:27017 -v ~/db:/data/db --name bankdomain_mongo bankdomain/mongo

docker run -it --network=mybridge -p 9090:9090 -p 9091:9091 -v ~/model:/media/diego/QData/bankdomain/model/: --name bankdomain_model bankdomain/model 
~~~~

~~~~
docker exec -it bankdomain_mongo /bin/sh /app/restore_db.sh s3://bankdomain/bankdomain-mongo-19-01-03-09-16.tgz 

In bankdomain_model
/app/src/restore_model.sh s3://bankdomain/techarticles-model-18-12-28-21-00.tgz


OR

In bankdomain_model
/app/src/setup_db.sh
/app/src/setup_archive.sh 

~~~~

~~~~
In bankdomain_model
/app/src/start_app.sh
~~~~

