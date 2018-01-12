# How to Create a Private Python Package Repository

	$ cd 18-pypi-repository
    $ python setup.py sdist

A tar.gz file will be generated at `~/pip_next_example/dist/`

Next install virtualenv if it’s not already installed:

    $ pip install virtualenv

Create a new directory which will be used to hold Python packages as well as files used by the web server. Create a new virtual environment called venv inside this directory, then activate:

    $ mkdir ~/packages
    $ cd packages
    $ virtualenv venv
    $ source venv/bin/activate

Download the package through pip in the newly created virtual environment:

    $ pip install pypiserver

    $ mv ~/dev/pip_next_example/dist/pip_next_example-0.1.tar.gz ~/packages/

Start the server:

    $ pypi-server -p 8082 ~/packages
    
    $ curl http://192.168.10.103:8082/simple/

Install the package:

    $ pip install --extra-index-url http://localhost:8082/simple/ --trusted-host localhost pip_next_example

Alternatively using pip.conf

    $ mkdir ~/.pip && cd ~/.pip
    $ touch pip.conf && vi pip.conf

Paste this into pip.conf:

    [global]
    extra-index-url = http://localhost:8082/
    trusted-host = localhost

And install again:

    $ pip install pip_next_example
    
Test the installation:

    $ pip freeze
    $ output: pip-next-example==0.1
    $ python
    $ >>> from pip_next_example import hello
    $ >>> hello.Hello().say_hello()
    $ 'Hello, Nextinterfaces!'

Based on following tutorials:

- https://linode.com/docs/applications/project-management/how-to-create-a-private-python-package-repository/
- http://peterdowns.com/posts/first-time-with-pypi.html


