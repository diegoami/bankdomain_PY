BFILE=/media/diego/QData/bankdomain/bankdomain_dump.tgz
BDIR=/media/diego/QData/bankdomain/dump/
rm -rf $BDIR
mkdir -p $BDIR
rm $BFILE
aws s3 cp s3://bankdomain/$1 $BFILE
tar xvf $BFILE -C /
cd /media/diego/QData/bankdomain/
mongorestore



