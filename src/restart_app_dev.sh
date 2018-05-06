
nohup gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:9090  -w 1 --error-logfile=gunicorn-error.log --access-logfile=gunicorn-access.log &
