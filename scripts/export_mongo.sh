BFILE=/media/diego/QData/bankdomain/bankdomain_dump.tgz
BDIR=/media/diego/QData/bankdomain/dump/
rm -rf $BDIR
mkdir -p $BDIR
/usr/bin/mongodump -d bankdomain -o $BDIR
rm $BFILE
tar cvfz $BFILE $BDIR
FDTIME="$(date +%y-%m-%d-%H-%M)"
aws s3 cp $BFILE s3://bankdomain/bankdomain-mongo-$FDTIME.tgz


