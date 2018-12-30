MFILE=/media/diego/QData/bankdomain/bankdomain_model.tgz
rm $MFILE
aws s3 cp $1 $MFILE
tar xvf $MFILE -C /


