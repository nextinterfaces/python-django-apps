from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import DiscoveryDocument, TokenManager, Struct, Profile
from .tokens import token_validation
from .openid import call_token_endpoint

import requests
import json
import sys


# GLOBALS
config = Struct(**settings.OKTA_JSON)
okta_config = Struct(**config.oktaSample)


def scenarios_controller(request):
    return render(
        request,
        settings.TEMPLATES_DIR + '/overview.mustache',
        {'config': okta_config, 'user': {}}
    )
    

def login_redirect_controller(request):
    return render(
        request,
        settings.TEMPLATES_DIR + '/login-redirect.mustache',
        {'config': okta_config, 'user': {}}
    )


def login_custom_controller(request):
    return render(
        request,
        settings.TEMPLATES_DIR + '/login-custom.mustache',
        {'config': okta_config, 'user': {}}
    )


def profile_controller(request):
    # Verify user is signed in and display profile contents

    try:
        user = User.objects.get(username=request.user)
    except ObjectDoesNotExist:
        return redirect('/')

    params = {
        'email': request.user,
        'claims': Struct(**user.profile.tokens.claims)
    }

    return render(
        request,
        settings.TEMPLATES_DIR + '/profile.mustache',
        {'config': okta_config, 'user': params}
    )

def callback_controller(request):
    # Handles the token exchange from the redirect

    state = None
    nonce = None

    # Get state and nonce from cookie
    if ('okta-oauth-state' in request.COOKIES and
            'okta-oauth-nonce' in request.COOKIES):
        # Current AuthJS Cookie Setters
        state = request.COOKIES['okta-oauth-state']
        nonce = request.COOKIES['okta-oauth-nonce']
    else:
        return HttpResponse('Error setting and/or retrieving cookies',
                            status=401)

    # Verify state
    if not state or request.GET['state'] != state:
        return HttpResponse('State from cookie does not match query state',
                            status=401)

    # Verify code exists
    if 'code' not in request.GET:
        return HttpResponse('Code was not returned', status=401)

    # Setup Token Request
    token_endpoint = '{}/v1/token?'.format(okta_config.oidc['issuer'])

    tokens = call_token_endpoint(
        token_endpoint,
        request.GET['code'],
        okta_config.oidc)

    if not tokens:
        # No tokens returned from /token endpoint
        return HttpResponse('Error retrieving tokens', status=401)

    if 'id_token' not in tokens:
        # id_token was not returned
        return HttpResponse('No id_token in response from /token endpoint',
                            status=401)

    if tokens['id_token'] is None:
        # id_token is set to None
        return HttpResponse('id_token is None', status=401)

    message, status = token_validation(tokens, okta_config, nonce)

    if status == 401:
        return HttpResponse(message, status=status)

    claims = message

    user = validate_user(claims)
    if user is None:
        # Verify user authenticated
        return HttpResponse('No user object', status=401)

    user.profile.tokens.set_id_token(tokens['id_token'])
    user.profile.tokens.set_claims(claims)

    if 'access_token' in tokens:
        user.profile.tokens.set_access_token(tokens['access_token'])

    # Log the user in
    login(request, user)

    return redirect('/authorization-code/profile')


def logout_controller(request):
    # Log user out

    # Clear existing user
    user = User.objects.get(username=request.user).delete()
    logout(request)

    return redirect('/')


def validate_user(claims):
    # Create user for django session

    user = authenticate(
        username=claims['email'],
        password=claims['sub']
    )

    if user is None:
        # Create user
        new_user = User.objects.create_user(
            claims['email'],
            claims['email'],
            claims['sub']
        )

        user = authenticate(
            username=claims['email'],
            password=claims['sub']
        )

    # Update user profile
    if not hasattr(user, 'profile'):
        profile = Profile()
        profile.user = user
        profile.save()

    return user
