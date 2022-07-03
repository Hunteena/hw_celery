# Домашнее задание к лекции Celery

Redis и postgres запускаются в docker-контейнерах из корневой директории проекта
```
docker-compose up
```

Для запуска celery
```
cd app
celery -A flask_celery:celery_app worker
```



Для запуска отладочного почтового сервера
```
python3 -m smtpd -c DebuggingServer -n localhost:1025
```

Скрипт *client.py* создаёт в базе одного пользователя, логинится под ним и создаёт объявление.
Скрипт *client_celery.py* отправляет почту всем пользователям из базы.
