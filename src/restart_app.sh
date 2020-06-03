#!/bin/bash

cd /home/ubuntu/projects/bankdomain_PY/src/
source /home/ubuntu/anaconda3/bin/activate faqportal2
nohup /home/ubuntu/anaconda3/envs/faqportal2/bin/gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:9090 -w 1 --error-logfile=gunicorn-error.log --access-logfile=gunicorn-access.log &
