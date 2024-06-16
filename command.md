py manage.py runserver 9000 

celery -A Job_Application worker -l info -P gevent
celery -A Job_Application beat -l info