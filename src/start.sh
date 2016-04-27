source /root/webproject/env/bin/activate
export C_FORCE_ROOT="true"
service mysql restart
service nginx restart
service redis restart
/etc/init.d/postfix restart
gunicorn --reload -b localhost:8080 application.wsgi:application -w 4
