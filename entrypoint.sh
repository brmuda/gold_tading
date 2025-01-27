#!/bin/bash

python manage.py makemigrations trading
python manage.py migrate
python manage.py shell -c "from trading.models import User; User.objects.create_superuser('admin', '', '123456', phone_number='09019601335') if not User.objects.filter(username='admin').exists() else None"

python manage.py runserver 0.0.0.0:8000