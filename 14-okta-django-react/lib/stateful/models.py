# Create your models here.
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

import requests


class DiscoveryDocument:
    # Find the OIDC metadata through discovery

    def __init__(self, base_url):
        r = requests.get(base_url + '/.well-known/openid-configuration')
        self.json = r.json()

    def getJson(self):
        return self.json


class TokenManager:
    # Store idToken, accessToken, and claims for user session object

    def __init__(self):
        self.idToken = None
        self.accessToken = None
        self.claims = None

    def set_id_token(self, token):
        self.idToken = token

    def set_access_token(self, token):
        self.accessToken = token

    def set_claims(self, claims):
        self.claims = claims

    def get_json(self):
        response = {}
        if self.idToken:
            response['idToken'] = self.idToken

        if self.accessToken:
            response['accessToken'] = self.accessToken

        if self.claims:
            response['claims'] = self.claims
        return response


class Struct:
    # Convert dict into object

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Profile(models.Model):
    # Extended user model to contain tokens

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = TokenManager()
