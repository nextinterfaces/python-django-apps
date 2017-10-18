python django helloworld
==========

A Django 'hello world' example.

Install Django if not present:

    $ sudo pip install django

Check django version:

    $ python -c "import django; print(django.get_version())"
    or $ django-admin.py version

For run this example need to install Django framework execute the follow command::

    $ sudo pip install -r requirements.txt

And later followed by:

    $ python manage.py migrate

At which point you should see:

    Operations to perform:
      Apply all migrations: admin, contenttypes, sites, auth, sessions
    Running migrations:
      Rendering model states... DONE
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying sessions.0001_initial... OK
      Applying sites.0001_initial... OK
      Applying sites.0002_alter_domain_unique... OK

After which you can run:

    $ python manage.py runserver

And open the following URL in your web browser:

 - http://127.0.0.1:8000/