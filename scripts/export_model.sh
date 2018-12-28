MFILE=/media/diego/QData/bankdomain/bankdomain_model.tgz
MDIR=/media/diego/QData/bankdomain/model/
rm $MFILE
tar cvfz $MFILE $MDIR
FDTIME="$(date +%y-%m-%d-%H-%M)"
aws s3 cp $MFILE s3://bankdomain/bankdomain-model-$FDTIME.tgz


