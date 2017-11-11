from django.conf import settings

from jose import jwt, jws
from datetime import datetime
from datetime import timedelta

import calendar
import requests


def fetch_jwk_for(issuer, id_token=None):
    if id_token is None:
        raise NameError('id_token is required')

    # FIXME: This should be pulled from the OpenID connect Discovery Document
    jwks_uri = '{}/v1/keys'.format(issuer)

    unverified_header = jws.get_unverified_header(id_token)
    key_id = None

    if 'kid' in unverified_header:
        key_id = unverified_header['kid']
    else:
        raise ValueError('The id_token header must contain a "kid"')

    if key_id in settings.PUBLIC_KEY_CACHE:
        return settings.PUBLIC_KEY_CACHE[key_id]

    r = requests.get(jwks_uri)
    jwks = r.json()

    for key in jwks['keys']:
        jwk_id = key['kid']
        settings.PUBLIC_KEY_CACHE[jwk_id] = key

    if key_id in settings.PUBLIC_KEY_CACHE:
        return settings.PUBLIC_KEY_CACHE[key_id]
    else:
        raise RuntimeError('Unable to fetch public key from jwks_uri')


def token_validation(tokens, okta_config, nonce):
    # Perform token validation

    try:
        clock_skew = 300
        jwks_with_public_key = fetch_jwk_for(okta_config.oidc['issuer'], tokens['id_token'])

        jwt_kwargs = {
            'algorithms': jwks_with_public_key['alg'],
            'options': {
                'verify_at_hash': False,
                # Used for leeway on the 'exp' claim
                'leeway': clock_skew
            },
            'issuer': okta_config.oidc['issuer'],
            'audience': okta_config.oidc['clientId']
        }

        if 'access_token' in tokens:
            jwt_kwargs['access_token'] = tokens['access_token']

        claims = jwt.decode(
            tokens['id_token'],
            jwks_with_public_key,
            **jwt_kwargs)

        if nonce != claims['nonce']:
            return 'invalid nonce', 401

        # Validate 'iat' claim
        plus_time_now_with_clock_skew = (datetime.utcnow() +
                                         timedelta(seconds=clock_skew))
        plus_acceptable_iat = calendar.timegm(
            (plus_time_now_with_clock_skew).timetuple())

        if 'iat' in claims and claims['iat'] > plus_acceptable_iat:
            return 'invalid iat claim', 401

        return claims, 200

    except Exception as err:
        return str(err), 401
