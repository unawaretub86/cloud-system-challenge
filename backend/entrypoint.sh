#!/bin/sh

echo "Esperando a que la base de datos esté disponible..."
python -c "
import sys
import time
import psycopg2

while True:
    try:
        psycopg2.connect(
            dbname='todo_db',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        break
    except psycopg2.OperationalError:
        sys.stderr.write('Esperando a que la base de datos esté disponible...\n')
        time.sleep(1)
"
echo "Base de datos disponible!"

echo "Aplicando migraciones..."
python manage.py migrate

echo "Verificando superusuario..."
python -c "
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superusuario creado')
else:
    print('Superusuario ya existe')
"

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."
gunicorn backend.config.wsgi:application --bind 0.0.0.0:8000