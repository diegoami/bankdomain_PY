

## LEGACY SCRIPTS (old scripts)

* import_all.py
* process_questions.py
* print_all.py
* create_model.py

## DOCKER
~~~~

docker build -f docker/mongo/Dockerfile --build-arg DB_ARCHIVE_NAME="s3://bankdomain/techarticles-mongo-18-12-28-21-06.tgz" --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/mongo .


docker build -f docker/portal/Dockerfile --build-arg SECRET_KEY=... --build-arg MODEL_ARCHIVE_NAME="s3://bankdomain/techarticles-model-18-12-28-21-00.tgz" --build-arg AWS_ACCESS_KEY_ID=... --build-arg AWS_SECRET_ACCESS_KEY=... --tag bankdomain/model .

docker network create -d bridge mybridge

docker run -d --network=mybridge -p 27017:27017 --name bankdomain_mongo bankdomain/mongo

docker exec -it bankdomain_mongo /bin/sh /app/entry_point.sh

docker run -it --network=mybridge -p 9090:9090 -p 9091:9091 --name bankdomain_model bankdomain/model /bin/cd /app/src/entry_point.sh
~~~~