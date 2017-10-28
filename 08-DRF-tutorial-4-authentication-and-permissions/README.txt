
## MySQL setup

    - http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django

## Django RESTFramework tutorials

    - http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

## Django tutorials

    $ /usr/local/bin/mysql.server start
    $ truncate/delete database or tables
    $ delete migrations
    $ python3 -m venv env_dev
    $ source env_dev/bin/activate
    $ pip install -r requirements/dev.txt

    $ python3 manage.py makemigrations snippets
    $ python3 manage.py migrate

    $ python3 manage.py createsuperuser
    --> admin:canadacanada

    $ http http://127.0.0.1:8000/snippets/
    $ http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
    $ http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
    $ http http://127.0.0.1:8000/snippets.json  # JSON suffix
    $ http http://127.0.0.1:8000/snippets.api   # Browsable API suffix


    $ http -a admin:canadacanada POST http://127.0.0.1:8000/snippets/ code="print 789"
