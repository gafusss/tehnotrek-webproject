#!/usr/bin/env bash
source /root/webproject/env/bin/activate
export C_FORCE_ROOT="true"
service mysql restart
service nginx restart
service redis restart
/etc/init.d/postfix restart
./manage.py collectstatic --noinput
gunicorn --reload -b localhost:8080 application.wsgi:application -w 4
