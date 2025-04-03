#!/bin/bash
set -e


if [ "$CLEAR_MIGRATIONS" = "true" ]; then
  echo "Clearing old migrations..."
  rm -rf manage_user/migrations/
fi

echo "Running migrations..."
python manage.py migrate

if [ "$RUN_TESTS" = "true" ]; then
  echo "Running tests..."
  python manage.py test
  if [ $? -ne 0 ]; then
    echo "❌ Test step failed, please fix before pushing."
    exit 1
  fi
fi

if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --no-input || echo "Superuser already exists."
fi

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
