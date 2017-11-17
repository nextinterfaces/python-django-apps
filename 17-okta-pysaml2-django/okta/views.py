from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT, entity
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
import requests
from .user_mixins import UserMixin

IDP_NAME = 'example-okta-com'
metadata_url_for = {
    'example-okta-com': 'https://dev-<id>.oktapreview.com/app/<id>/sso/saml/metadata'
}
user_store = {}


def saml_client_for(idp_name=None):
    acs_url = 'http://localhost:8001/saml/sso/example-okta-com'
    https_acs_url = 'https://localhost:8001/saml/sso/example-okta-com'

    rv = requests.get(metadata_url_for[idp_name])

    settings = {
        'metadata': {
            'inline': [rv.text],
        },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST),
                        (https_acs_url, BINDING_HTTP_REDIRECT),
                        (https_acs_url, BINDING_HTTP_POST)
                    ],
                },
                # Don't verify that the incoming requests originate from us via
                # the built-in cache for authn request ids in pysaml2
                'allow_unsolicited': True,
                # Don't sign authn requests, since signed requests only make
                # sense in a situation where you control both the SP and IdP
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
    }
    spConfig = Saml2Config()
    spConfig.load(settings)
    spConfig.allow_unknown_attributes = True
    saml_client = Saml2Client(config=spConfig)
    return saml_client


class User(UserMixin):
    def __init__(self, user_id):
        user = {}
        self.id = None
        self.first_name = None
        self.last_name = None
        try:
            user = user_store[user_id]
            self.id = unicode(user_id)
            self.first_name = user['first_name']
            self.last_name = user['last_name']
        except:
            pass


def load_user(user_id):
    return User(user_id)


def main_page(request):
    return render(request, 'okta-index.html', {})


# https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set
# @csrf_exempt
# @ensure_csrf_cookie
# Fixme "CSRF token missing or incorrect."
@csrf_exempt  # this is a workaround
@require_http_methods("POST")
def login_idp_initiated(request):
    saml_client = saml_client_for(IDP_NAME)
    SAMLResponse = request.POST.get('SAMLResponse')
    authn_response = saml_client.parse_authn_request_response(
        SAMLResponse,
        entity.BINDING_HTTP_POST)
    authn_response.get_identity()
    user_info = authn_response.get_subject()
    username = user_info.text

    # This is what as known as "Just In Time (JIT) provisioning".
    # What that means is that, if a user in a SAML assertion
    # isn't in the user store, we create that user first, then log them in
    if username not in user_store:
        user_store[username] = {
            'first_name': authn_response.ava['FirstName'][0],
            'last_name': authn_response.ava['LastName'][0],
        }
    redirect_url = '/saml'
    return redirect(redirect_url, code=302)


def login_sp_initiated(request):
    saml_client = saml_client_for(IDP_NAME)
    reqid, info = saml_client.prepare_for_authenticate()

    redirect_url = None
    # Select the IdP URL to send the AuthN request to
    for key, value in info['headers']:
        if key is 'Location':
            redirect_url = value

    response = redirect(redirect_url, code=302)
    # http://stackoverflow.com/a/5494469 Cache-Control or Expires
    response['Cache-Control'] = 'no-cache, no-store'
    response['Pragma'] = 'no-cache'
    return response


def logout(request):
    # logout_user()
    return render(request, 'okta-logout.html', {})
