source /root/webproject/env/bin/activate
service mysql restart
service nginx restart
gunicorn --reload -b localhost:8080 application.wsgi:application -w 4
