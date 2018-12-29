echo $1
aws s3 cp $1 /media/diego/QData/bankdomain/bankdomain_model.tgz
tar xvf /media/diego/QData/bankdomain/bankdomain_model.tgz -C /
