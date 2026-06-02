#!/bin/sh
set -e

# Ожидание PostgreSQL
until nc -z -v -w30 "$DB_HOST" "$DB_PORT"
do
  echo "Waiting for database connection..."
  sleep 1
done

# Ожидание Redis
until nc -z -v -w30 redis 6379
do
  echo "Waiting for redis..."
  sleep 1
done

# Выполнение миграций
python manage.py migrate --noinput

exec "$@"