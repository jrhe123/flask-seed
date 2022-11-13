### Flask with MySQL, MongoDB, Redis examples

1. export FLASK_APP=app.py
2. export FLASK_ENV=development
3. export FLASK_DEBUG=1

flask run --port=5000


### Celery - background job (with redis)
doc: https://github.com/soumilshah1995/Python-Flask-Redis-Celery-Docker/blob/main/Part1/flask_app/app.py

1. cd simplez_worker
2. celery -A tasks worker --loglevel=info
3. test calls
4. http://localhost:5000/simple_start_task
5. http://localhost:5000/simple_task_status/78bbe7bc-deeb-4958-b029-58e59c2de7ca
6. http://localhost:5000/simple_task_result/78bbe7bc-deeb-4958-b029-58e59c2de7ca


### Docker setup:
1. mysql: 33066 -> 3306 (create schema & migrate tables)
2. redis: 6380 -> 6379
3. mongo: 27017 -> 27017
