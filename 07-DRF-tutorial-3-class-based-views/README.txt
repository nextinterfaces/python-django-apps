
## MySQL setup

    - http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django

## Django RESTFramework tutorials

    - http://www.django-rest-framework.org/tutorial/3-class-based-views/

## Django tutorials

    $ /usr/local/bin/mysql.server start
    $ python3 -m venv env_dev           # ! Important to set python3 env
    $ source env_dev/bin/activate
    $ pip install -r requirements/dev.txt

    $ python manage.py makemigrations snippets
    $ python manage.py migrate
    $ python manage.py createsuperuser
    --> admin:canadacanada

    $ python manage.py runserver 0.0.0.0:8000

    $ http http://127.0.0.1:8000/snippets/
    $ http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
    $ http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
    $ http http://127.0.0.1:8000/snippets.json  # JSON suffix
    $ http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
