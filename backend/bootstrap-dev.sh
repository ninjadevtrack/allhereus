# wait for database - https://www.stavros.io/posts/how-deploy-django-docker/
while ! nc -w 1 -z ${DB_HOST} 5432
    do sleep 0.1
done
./manage.py shell < set_server.py
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
