echo $1
aws s3 cp $1 /media/diego/QData/bankdomain/bankdomain_dump.tgz
tar xvf /media/diego/QData/bankdomain/bankdomain_dump.tgz -C /
cd /media/diego/QData/bankdomain/
mongorestore

