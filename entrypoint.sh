#!/bin/sh
set -e

until nc -z -v -w30 "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database..."
  sleep 1
done

until nc -z -v -w30 redis 6379; do
  echo "Waiting for redis..."
  sleep 1
done

python manage.py migrate --noinput

exec "$@"