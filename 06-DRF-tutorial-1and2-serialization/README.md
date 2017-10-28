
## MySQL setup

- http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django

## Django RESTFramework tutorials

- http://www.django-rest-framework.org/tutorial/3-class-based-views/

## Django tutorials

    $ /usr/local/bin/mysql.server start
    $ python3 -m venv env_dev ## Important to set python3 to env
    $ source env_dev/bin/activate
    $ pip install -r requirements.txt

    $ django-admin.py startproject tutorial
    # python manage.py startapp snippets

    $ python manage.py makemigrations snippets
    $ python manage.py migrate


    $ python manage.py shell

    $ python manage.py runserver 0.0.0.0:8000



    $ python3 manage.py createsuperuser
    --> admin:canadacanada


    $ http http://127.0.0.1:8000/snippets/
    $ http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
    $ http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
    $ http http://127.0.0.1:8000/snippets.json  # JSON suffix
    $ http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
