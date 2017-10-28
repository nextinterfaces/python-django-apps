
    - http://www.django-rest-framework.org/tutorial/3-class-based-views/

    $ /usr/local/bin/mysql.server start
    $ python3 -m venv env_dev
    $ source env_dev/bin/activate
    $ pip install -r requirements/dev.txt

    $ python manage.py makemigrations snippets
    $ python manage.py migrate

    $ python manage.py createsuperuser

    $ http http://127.0.0.1:8000/snippets/
    $ http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
    $ http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
    $ http http://127.0.0.1:8000/snippets.json  # JSON suffix
    $ http http://127.0.0.1:8000/snippets.api   # Browsable API suffix