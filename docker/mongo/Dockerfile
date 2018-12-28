FROM mongo


RUN apt-get update && apt-get install -y python python-pip curl unzip groff
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install awsebcli
RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"&& \
    unzip awscli-bundle.zip && \
    ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws


ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG DB_ARCHIVE_NAME

RUN mkdir -p ~/.aws
RUN mkdir -p /media/diego/QData/bankdomain/


RUN echo "[default]" >> ~/.aws/credentials
RUN echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
RUN echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials

RUN aws s3 cp $DB_ARCHIVE_NAME /media/diego/QData/bankdomain/bankdomain_dump.tgz
RUN tar xvf /media/diego/QData/bankdomain/bankdomain_dump.tgz -C /

EXPOSE 27017



