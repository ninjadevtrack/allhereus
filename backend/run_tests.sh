# wait for database - https://www.stavros.io/posts/how-deploy-django-docker/
while ! nc -w 1 -z ${DB_HOST} 5432
    do sleep 0.1
done
python manage.py collectstatic --noinput
pytest -c pytest.ini --ignore=ednudge-sdk-python
