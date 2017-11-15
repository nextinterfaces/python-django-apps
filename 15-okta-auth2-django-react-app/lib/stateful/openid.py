from requests.auth import HTTPBasicAuth

import requests
import base64
import urllib


def call_token_endpoint(url, code, config):
    """ Call /token endpoint
        Returns accessToken, idToken, or both
    """
    auth = HTTPBasicAuth(config['clientId'], config['clientSecret'])
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Connection': 'close'
    }

    # Query string to pass yakback test
    params = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(
        urllib.parse.quote_plus(code),
        urllib.parse.quote_plus(config['redirectUri'])
    )

    url_encoded = '{}{}'.format(url, params)

    # Send token request
    r = requests.post(url_encoded, auth=auth, headers=header)

    return r.json()
