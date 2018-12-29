

## SET UP DATABASE

Make sure you set up an instance of mongo. The database will be called bankdomain

The documents are contained in the github repository: _https://github.com/diegoami/bankdomain.git_

Make sure that the documents directory links to   _/media/diego/QData/bankdomain/docs/qa_documents_ .

~~~~
git clone https://github.com/diegoami/bankdomain.git
ln -s $(pwd)/bankdomain/qa_documents /media/diego/QData/bankdomain/docs/qa_documents 
~~~~

## DOCKER
~~~~

docker build -f docker/mongo/Dockerfile  --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/mongo .

docker build -f docker/portal/Dockerfile --build-arg SECRET_KEY=... --build-arg  --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/model .

docker network create -d bridge mybridge

docker run -d --network=mybridge -p 27017:27017 --name bankdomain_mongo bankdomain/mongo


docker run -it --network=mybridge -p 9090:9090 -p 9091:9091 --name bankdomain_model bankdomain/model 
~~~~

~~~~
docker exec -it bankdomain_mongo /bin/sh /app/src/restore_db.sh s3://bankdomain/techarticles-mongo-18-12-28-21-06.tgz 
docker exec -it bankdomain_model /bin/sh /app/restore_model.sh s3://bankdomain/techarticles-model-18-12-28-21-00.tgz


OR

docker exec -it bankdomain_model /bin/sh /app/setup_db.sh
docker exec -it bankdomain_model /bin/sh /app/setup_archive.sh 

~~~~

~~~~
docker exec -it bankdomain_model /bin/sh /app/src/start_app.sh
~~~~

