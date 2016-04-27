source /root/webproject/env/bin/activate
export C_FORCE_ROOT="true"
./manage.py celery worker
