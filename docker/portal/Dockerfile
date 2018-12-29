FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential gcc
RUN apt-get install -y python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN ln -s /usr/bin/python3.6 /usr/bin/python

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install cython==0.29.2
RUN pip install numpy==1.15.4

RUN pip install -r requirements.txt
RUN python3.6 -m spacy download de

RUN mkdir -p /media/diego/QData/bankdomain/keys/
RUN mkdir -p  /media/diego/keys/
RUN mkdir ~/.aws

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ARG MODEL_ARCHIVE_NAME
ARG SECRET_KEY

RUN echo "[default]" >> ~/.aws/credentials
RUN echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
RUN echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials

RUN aws s3 cp $MODEL_ARCHIVE_NAME /media/diego/QData/bankdomain/bankdomain_model.tgz
RUN tar xvf /media/diego/QData/bankdomain/bankdomain_model.tgz -C /

RUN echo "secret_key : $SECRET_KEY" >> /media/diego/keys/db_coords.yml


COPY . /app


RUN cd /app && sed -i.bak s/localhost/bankdomain_mongo/g config.yml
RUN cp /app/docker/portal/entry_point.sh /app/src/

EXPOSE 9091
EXPOSE 9090



