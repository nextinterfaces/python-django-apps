# How to make pip installing packages from Artifactory's repo

### Local repo
Make a local python repo on your machine. You can use this [sample pip repo](https://github.com/nextinterfaces/python-django-apps/tree/master/18-pypi-repository).

### Start Artifactory server

	$ cd <ARTIFACTORY_HOME> && ./bin/artifactory.sh

### Deploy to Artifactory

To deploy packages using `setuptools` you need to add an Artifactory repository to the `~/.pypirc` file (usually located in your home directory):

	$ vi ~/.pypirc
	
	[distutils]
	index-servers = local
	[local]
	repository: http://localhost:8081/artifactory/api/pypi/pypi-local
	username: admin <admin being default user>
	password: password <password being the default password>

### Deploy the egg
To deploy a python egg to Artifactory, after changing the .pypirc file, run the following command:

	$ cd <sample_repo>
	$ python setup.py sdist upload -r local

where `local` is the index server you defined in `~/.pypirc`.

### Configure pip to resolve from Artifactory local
Create config file for pip that will resolve the artifactory server from Pypi virtual repository (aggregating `pypi-local` and `pypi-remote`):
	
	$ vi ~/.pip/pip.conf
	
	[global]
	index-url = http://localhost:8081/artifactory/api/pypi/pypi/simple
	

### And pip install

	$ pip install pip_next_example==0.1
	
### Tutorial
[Setting up Artifactory 5 as a PyPI repository in under one minute](https://www.youtube.com/watch?v=WSUjbnfWxvg)


