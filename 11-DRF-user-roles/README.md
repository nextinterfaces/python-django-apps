
## MySQL setup

- http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django

## Django RESTFramework tutorial

- http://www.django-rest-framework.org/tutorial/3-class-based-views/

## Setup

    $ /usr/local/bin/mysql.server start
    $ python3 -m venv env_dev           # ! Important to set python3 env
    $ source env_dev/bin/activate
    $ pip install -r requirements.txt

    $ django-admin.py startproject tutorial
    # python manage.py startapp snippets

    $ python manage.py makemigrations snippets
    $ python manage.py migrate

    $ python manage.py runserver 0.0.0.0:8000

    $ http http://127.0.0.1:8000/snippets/
    # http http://127.0.0.1:8000/snippets.json
    $ http http://127.0.0.1:8000/snippets.api

    $ http --debug --form POST http://127.0.0.1:8000/snippets/ code="print 444444"
    $ http --debug --json POST http://127.0.0.1:8000/snippets/ code="print 456"
    $ http --debug --json POST http://127.0.0.1:8000/snippets/ code="print 777"