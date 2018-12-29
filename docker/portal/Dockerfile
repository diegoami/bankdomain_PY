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
ARG SECRET_KEY

RUN echo "[default]" >> ~/.aws/credentials
RUN echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
RUN echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials

RUN echo "secret_key : $SECRET_KEY" >> /media/diego/keys/db_coords.yml

RUN mkdir -p /media/diego/QData/bankdomain/docs/ && cd /media/diego/QData/bankdomain/docs/  && git clone https://github.com/diegoami/bankdomain.git
RUN mv /media/diego/QData/bankdomain/docs/bankdomain/qa_documents /media/diego/QData/bankdomain/docs/qa_documents

COPY . /app

RUN cd /app && sed -i.bak s/localhost/bankdomain_mongo/g config.yml
RUN cp /app/docker/portal/*.sh /app/src

EXPOSE 9091
EXPOSE 9090



