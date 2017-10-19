Django REST framework application
=========

A REST application written in Python, Django and REST-framework based on [This tutorial](http://www.django-rest-framework.org/tutorial/quickstart/).

Installation
------------

    $ virtualenv env

    $ source env/bin/activate

    $ pip install -r requirements.txt

Check django version:

    $ python -c "import django; print(django.get_version())"
    $ python -c "import rest_framework; print rest_framework.VERSION"

Start server:

    $ python manage.py runserver

Test API using HTTPie:

    $ bash  http -a admin:password123 http://127.0.0.1:8000/users/

Or open in web browser:

    - http://127.0.0.1:8000/users/
