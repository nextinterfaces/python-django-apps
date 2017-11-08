# Django app using models and admin

Based on https://docs.djangoproject.com/en/1.11/intro/tutorial03/

Using sql lite database

    $ python3 -m venv .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt

    django-admin startproject mysite

    cd mysite

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
