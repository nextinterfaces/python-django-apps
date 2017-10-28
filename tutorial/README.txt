

    $ /usr/local/bin/mysql.server start
    $ python3 -m venv env_dev
    $ source env_dev/bin/activate
    $ pip install -r requirements/dev.txt

    $ python manage.py makemigrations snippets
    $ python manage.py migrate

    $ python manage.py createsuperuser

    $ http http://127.0.0.1:8000/snippets/