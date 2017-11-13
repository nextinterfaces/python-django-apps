# Okta Django React app

Based on this:

    - https://github.com/okta/samples-python-django
    - https://github.com/okta/samples-js-react

Using React front-end and Django back-end

To start Django:

    $ npm install
    
    $ bin/init

    $ bin/start


To run with mock-okta:

    Modify .samples.config.json

    $ bin/start-mock

To run against okta.com

    1. Create an app in okta using:

        - https://github.com/okta/samples-python-django#quick-start

    2. Modify .samples.config.json with the app configurations

    After which `$ bin/start` Django


To build client:

    $ bin/start-client