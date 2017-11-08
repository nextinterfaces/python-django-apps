# django-hello-world
The simplest possible Django 1.8 site.

This project is intended to be a very simple example site, using a standard django project layout, for testing Django deployment strategies.



    $ /usr/local/bin/mysql.server start
    $ python3 -m venv .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt


django-admin startproject mysite

python manage.py runserver

python manage.py startapp polls

python manage.py migrate

python manage.py makemigrations polls

python manage.py sqlmigrate polls 0001

python manage.py migrate

python manage.py shell

python manage.py createsuperuser
 --> admin/canadacanada

python manage.py runserver 0.0.0.0:8000

    $ python manage.py makemigrations snippets
    $ python manage.py migrate

    $ python manage.py runserver 0.0.0.0:8000