MFILE=/media/diego/QData/bankdomain/bankdomain_model.tgz
rm $MFILE
aws s3 cp s3://bankdomain/$1 $MFILE
tar xvf $MFILE -C /


