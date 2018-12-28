FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential gcc python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

COPY requirements.txt app/requirements.txt

WORKDIR /app
RUN pip install -r cython numpy
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

EXPOSE 9091
EXPOSE 9090



