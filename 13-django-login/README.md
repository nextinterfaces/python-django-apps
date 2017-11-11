## What's this repository about?

Example login system build on django

## How do I run this project locally?

    python3 -m venv .env

    source .env/bin/activate

    pip install -r requirements.txt

    python manage.py migrate

### 3. Create a user:

    python manage.py createsuperuser

    admin/canadacanada

### 4. Run the server:

    python manage.py runserver 0.0.0.0:8000

### 5. And open `http://127.0.0.1:8000/login` in your web browser.

From: http://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
