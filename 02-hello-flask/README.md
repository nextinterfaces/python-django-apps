

If you don't have virtualenv, install it using pip.

	$ sudo pip install virtualenv

Create an isolated Python environment, and install dependencies:

	$ virtualenv env
	$ source env/bin/activate
	$ pip install -r requirements.txt

Run the application:

	$ python main.py

In your web browser, enter the following address:

	$ http://localhost:8080