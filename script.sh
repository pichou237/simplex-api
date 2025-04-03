echo "Running migrations..."

python manage.py makemigrations manage_user 

python manage.py migrate

python manage.py test

python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
  echo " "
  echo "❌ Test step failed, please fix before pushing."
  exit 1
fi

gunicorn lebricoleur.wsgi:application --bind 0.0.0.0:8000