# AngularJS 1.x and django Sample Application

### Table of Contents

  - [Introduction](#introduction)
    - [Login Redirect](#1-login-redirect)
    - [Custom Login Form](#2-custom-login-form)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
  - [Front End](#front-end)
    - [Login Redirect](#login-redirect)
    - [Custom Login Form](#custom-login-form)
    - [Using a different front-end](#using-a-different-front-end)
  - [Back End](#back-end)
    - [Routes](#routes)
    - [Handle the Redirect](#handle-the-redirect)
    - [Code Exchange](#code-exchange)
    - [Validation](#validation)
  - [Set User Session](#set-user-session)
  - [Logout](#logout)
  - [Conclusion](#conclusion)
  - [Support](#support)
  - [License](#license)
  
## Introduction

This tutorial will demonstrate how to use OAuth 2.0 and OpenID Connect to add authentication to a python/django application.

### 1. Login Redirect

Users are redirected to your Okta organization for authentication.

<img src="docs/assets/redirect.png" width="300" />

After logging into your Okta organization, an authorization code is returned in a callback URL. This authorization code is then exchanged for an `id_token`.

### 2. Custom Login Form

The Okta Sign-In Widget is a fully customizable login experience. You can change how the widget [looks with CSS](http://developer.okta.com/code/javascript/okta_sign-in_widget#customizing-style-with-css) and [is configured with JavaScript](http://developer.okta.com/code/javascript/okta_sign-in_widget#customizing-widget-features-and-text-labels-with-javascript).

<img src="docs/assets/custom.png" width="300" />

This custom-branded login experience uses the [Okta Sign-In Widget](http://developer.okta.com/code/javascript/okta_sign-in_widget) to perform authentication, returning an authorization code that is then exchanged for an `id_token`.

## Prerequisites

This sample app depends on [Node.js](https://nodejs.org/en/) for front-end dependencies and some build scripts - if you don't have it, install it from [nodejs.org](https://nodejs.org/en/).

```bash
# Verify that node is installed
$ node -v
```

Then, clone this sample from GitHub and install the front-end dependencies:
```bash
# Clone the repo and navigate to the samples-python-django dir
$ git clone git@github.com:okta/samples-python-django.git && cd samples-python-django

# Install the front-end dependencies
[samples-python-django]$ npm install
```

Create an isolated virtual environment
Install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) via pip:
```
[samples-python-django]$ pip install virtualenv

# Create the virtual environment:
[samples-python-django]$ virtualenv venv

# Activate the virtual environment:
[samples-python-django]$ source venv/bin/activate

# When you are finished working inside of the virtual environment, you can deactivate it:

(venv)[samples-python-django]$ deactivate
```

## Quick Start

Start the back-end for your sample application with `npm start` or `python3 lib/manage.py runserver 3000`. This will start the app server on [http://localhost:3000](http://localhost:3000).

By default, this application uses a mock authorization server which responds to API requests like a configured Okta org - it's useful if you haven't yet set up OpenID Connect but would still like to try this sample. 

To start the mock server, run the following in a second terminal window:
```bash
# Starts the mock Okta server at http://127.0.0.1:7777
[samples-python-django]$ npm run mock-okta
```

If you'd like to test this sample against your own Okta org, navigate to the Okta Developer Dashboard and follow these steps:

1. Create a new **Web** application by selecting **Create New Application** from the *Applications* page.		
2. After accepting the default configuration, select **Create Application** to redirect back to the *General Settings* of your application.		
3. Copy the **Client ID** and **Client Secret**, as it will be needed for the client configuration.
4. Finally, navigate to `https://{yourOktaDomain}.com/oauth2/default` to see if the [Default Authorization Server](https://developer.okta.com/docs/api/resources/oauth2.html#using-the-default-authorization-server) is setup. If not, [let us know](mailto:developers@okta.com).

Then, replace the *oidc* settings in `.samples.config.json` to point to your new app:
```javascript
// .samples.config.json
{
  "oidc": {
    "oktaUrl": "https://{{yourOktaDomain}}.com",
    "issuer": "https://{{yourOktaDomain}}.com/oauth2/default",
    "clientId": "{{yourClientId}}",
    "clientSecret": "{{yourClientSecret}}",
    "redirectUri": "http://localhost:3000/authorization-code/callback"
  }
}
```

## Front-end

When you start this sample, the [AngularJS 1.x UI](https://github.com/okta/samples-js-angular-1) is copied into the `dist/` directory. More information about the AngularJS controllers and views are available in the [AngularJS project repository](https://github.com/okta/samples-js-angular-1/blob/master/README.md).

### Login Redirect

With AngularJS, we include the template directive `ng-click` to begin the login process. When the link is clicked, it calls the `login()` function defined in `login-redirect.controller.js`. Let’s take a look at how the `OktaAuth` object is created.

```javascript
// login-redirect.controller.js

class LoginRedirectController {
   constructor(config) {
    this.config = config;
  }
   $onInit() {
    this.authClient = new OktaAuth({
      url: this.config.oktaUrl,
      issuer: this.config.issuer,
      clientId: this.config.clientId,
      redirectUri: this.config.redirectUri,
      scopes: ['openid', 'email', 'profile'],
    });
  }
 
  login() {
    this.authClient.token.getWithRedirect({ responseType: 'code' });
  }
}
```

There are a number of different ways to construct the login redirect URL.

1. Build the URL manually
2. Use an OpenID Connect / OAuth 2.0 middleware library
3. Use [AuthJS](http://developer.okta.com/code/javascript/okta_auth_sdk)

In this sample, we use AuthJS to create the URL and perform the redirect. An `OktaAuth` object is instantiated with the configuration in `.samples.config.json`. When the `login()` function is called from the view, it calls the [`/authorize`](http://developer.okta.com/docs/api/resources/oauth2.html#authentication-request) endpoint to start the [Authorization Code Flow](https://tools.ietf.org/html/rfc6749#section-1.3.1).

You can read more about the `OktaAuth` configuration options here: [OpenID Connect with Okta AuthJS SDK](http://developer.okta.com/code/javascript/okta_auth_sdk#social-authentication-and-openid-connect).

**Important:** When the authorization code is exchanged for an `access_token` and/or `id_token`, the tokens **must** be [validated](#validation). We'll cover that in a bit.

### Custom Login Form
To render the [Okta Sign-In Widget](http://developer.okta.com/code/javascript/okta_sign-in_widget), include a container element on the page for the widget to attach to:

```html
<!-- overview.mustache -->
<div id="sign-in-container"></div>
```

Then, initialize the widget with the [OIDC configuration](https://github.com/okta/okta-signin-widget#openid-connect) options:
``` javascript
// login-custom.controller.js
class LoginCustomController {
  constructor(config) {
    this.config = config;
  }
 
  $onInit() {
    const signIn = new SignIn({
      baseUrl: this.config.oktaUrl,
      clientId: this.config.clientId,
      redirectUri: this.config.redirectUri,
      authParams: {
        issuer: this.config.issuer,
        responseType: 'code',
        scopes: ['openid', 'email', 'profile'],
      },
    });
    signIn.renderEl({ el: '#sign-in-container' }, () => {});
  }
}
```
To perform the [Authorization Code Flow](https://tools.ietf.org/html/rfc6749#section-1.3.1), we set the `responseType` to `code`. This returns an `access_token` and/or `id_token` through the [`/token`](http://developer.okta.com/docs/api/resources/oauth2.html#token-request) OpenID Connect endpoint.

**Note:** Additional configuration for the `SignIn` object is available at [OpenID Connect, OAuth 2.0, and Social Auth with Okta](https://github.com/okta/okta-signin-widget#configuration).

### Using a different front-end

By default, this end-to-end sample ships with our [Angular 1 front-end sample](https://github.com/okta/samples-js-angular-1). To run this back-end with a different front-end:

1. Choose the front-end

    | Framework | NPM module | Github |
    |-----------|------------|--------|
    | Angular 1 | [@okta/samples-js-angular-1](https://www.npmjs.com/package/@okta/samples-js-angular-1) | https://github.com/okta/samples-js-angular-1 |
    | React | [@okta/samples-js-react](https://www.npmjs.com/package/@okta/samples-js-react) | https://github.com/okta/samples-js-react |
    | Elm | [@okta/samples-elm](https://www.npmjs.com/package/@okta/samples-elm) | https://github.com/okta/samples-elm |


2. Install the front-end

    ```bash
    # Use the NPM module for the front-end you want to install. I.e. for React:
    [samples-python-django]$ npm install @okta/samples-js-react
    ```

3. Restart the server. You should be up and running with the new front-end!

## Back-end
To complete the [Authorization Code Flow](https://tools.ietf.org/html/rfc6749#section-1.3.1), your back-end server performs the following tasks:
  - Handle the [Authorization Code code exchange](https://tools.ietf.org/html/rfc6749#section-1.3.1) callback
  - [Validate](http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation) the `id_token`
  - Set `user` session in the app
  - Log the user out

### Routes
To render the AngularJS templates, we define the following django routes:

| Route                                 | Description                                                 |
| ------------------------------------- | ----------------------------------------------------------- |
| **authorization-code/login-redirect** | renders the [login redirect](#login-redirect) flow          |
| **authorization-code/login-custom**   | renders the [custom login](#custom-login-form) flow         |
| **authorization-code/callback**       | handles the redirect from Okta                              |
| **authorization-code/profile**        | renders the logged in state, displaying profile information |
| **authorization-code/logout**         | closes the `user` session                                   |

### Handle the Redirect
After successful authentication, an authorization code is returned to the redirectUri:
```
http://localhost:3000/authorization-code/callback?code={{code}}&state={{state}}
```

Two cookies are created after authentication: `okta-oauth-nonce` and `okta-auth-state`. You **must** verify the returned `state` value in the URL matches the `state` value created.

In this sample, we verify the state here:

```python
# views.py

if ('okta-oauth-state' in request.COOKIES and 'okta-oauth-nonce' in request.COOKIES):
    # Current AuthJS Cookie Setters
    state = request.COOKIES['okta-oauth-state']
    nonce = request.COOKIES['okta-oauth-nonce']
else:
    return HttpResponse('Error setting and/or retrieving cookies', status=401)
```

### Code Exchange
Next, we exchange the returned authorization code for an `id_token` and/or `access_token`. You can choose the best [token authentication method](http://developer.okta.com/docs/api/resources/oauth2.html#token-request) for your application. In this sample, we use the default token authentication method `client_secret_basic`:

```python
# openid.py

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

    params = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(
        urllib.parse.quote_plus(code),
        urllib.parse.quote_plus(config['redirectUri'])
    )

    url_encoded = '{}{}'.format(url, params)

    # Send token request
    r = requests.post(url_encoded, auth=auth, headers=header)

    return r.json()

```

A successful response returns an `id_token` which looks similar to:
```
eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwMHVpZDRCeFh3Nkk2VFY0bTBnMyIsImVtYWlsIjoid2VibWFzd
GVyQGNsb3VkaXR1ZGUubmV0IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInZlciI6MSwiaXNzIjoiaHR0cD
ovL3JhaW4ub2t0YTEuY29tOjE4MDIiLCJsb2dpbiI6ImFkbWluaXN0cmF0b3IxQGNsb3VkaXR1ZGUu
bmV0IiwiYXVkIjoidUFhdW5vZldrYURKeHVrQ0ZlQngiLCJpYXQiOjE0NDk2MjQwMjYsImV4cCI6MTQ0O
TYyNzYyNiwiYW1yIjpbInB3ZCJdLCJqdGkiOiI0ZUFXSk9DTUIzU1g4WGV3RGZWUiIsImF1dGhfdGltZSI
6MTQ0OTYyNDAyNiwiYXRfaGFzaCI6ImNwcUtmZFFBNWVIODkxRmY1b0pyX1EifQ.Btw6bUbZhRa89
DsBb8KmL9rfhku--_mbNC2pgC8yu8obJnwO12nFBepui9KzbpJhGM91PqJwi_AylE6rp-
ehamfnUAO4JL14PkemF45Pn3u_6KKwxJnxcWxLvMuuisnvIs7NScKpOAab6ayZU0VL8W6XAijQmnYTt
MWQfSuaaR8rYOaWHrffh3OypvDdrQuYacbkT0csxdrayXfBG3UF5-
ZAlhfch1fhFT3yZFdWwzkSDc0BGygfiFyNhCezfyT454wbciSZgrA9ROeHkfPCaX7KCFO8GgQEkGRoQ
ntFBNjluFhNLJIUkEFovEDlfuB4tv_M8BM75celdy3jkpOurg
```

### Validation
After receiving the `id_token`, we [validate](http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation) the token and its claims to prove its integrity. 

In this sample, we use a [JSON Object Signing and Encryption (JOSE)](https://github.com/mpdavis/python-jose) library to decode and validate the token.

There are a couple things we need to verify:

1. [Verify the signature](#verify-signature)
2. [Verify the *iss* (issuer), *aud* (audience), and *exp* (expiry) time](#verify-fields)
3. [Verify the *iat* (issued at) time](#verify-issued-time)
4. [Verify the *nonce*](#verify-nonce)

You can learn more about validating tokens in [OpenID Connect Resources](http://developer.okta.com/docs/api/resources/oidc.html#validating-id-tokens).

#### Verify signature
An `id_token` contains a [public key id](https://tools.ietf.org/html/rfc7517#section-4.5) (`kid`). To verify the signature, we use the [Discovery Document](http://developer.okta.com/docs/api/resources/oidc.html#openid-connect-discovery-document) to find the `jwks_uri`, which will return a list of public keys. It is safe to cache or persist these keys for performance, but Okta rotates them periodically. We strongly recommend dynamically retrieving these keys.

For example:
- If the `kid` has been cached, use it to validate the signature.
- If not, make a request to the `jwks_uri`. Cache the new `jwks`, and use the response to validate the signature.

```python
# tokens.py

def fetch_jwk_for(id_token=None):
    if id_token is None:
        raise NameError('id_token is required')

    jwks_uri = '{}/v1/keys'.format(issuer)

    unverified_header = jws.get_unverified_header(id_token)
    key_id = None

    if 'kid' in unverified_header:
        key_id = unverified_header['kid']
    else:
        raise ValueError('The id_token header must contain a "kid"')

    if key_id in settings.PUBLIC_KEY_CACHE:
        # If we've already cached this JWK, return it
        return settings.PUBLIC_KEY_CACHE[key_id]

    # If it's not in the cache, get the latest JWKS from /oauth2/default/v1/keys
    r = requests.get(jwks_uri)
    jwks = r.json()

    for key in jwks['keys']:
        jwk_id = key['kid']
        settings.PUBLIC_KEY_CACHE[jwk_id] = key

    if key_id in settings.PUBLIC_KEY_CACHE:
        return settings.PUBLIC_KEY_CACHE[key_id]
    else:
        raise RuntimeError('Unable to fetch public key from jwks_uri')
```

#### Verify fields

Verify the `id_token` from the [Code Exchange](#code-exchange) contains our expected claims:

  - The `issuer` is identical to the host where authorization was performed
  - The `clientId` stored in our configuration matches the `aud` claim
  - If the token expiration time has passed, the token must be revoked

```python
# tokens.py

# A clock skew of five minutes is considered to account for
# differences in server times
clock_skew = 300

jwks_with_public_key = fetch_jwk_for(tokens['id_token'])

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

claims = jwt.decode(
    tokens['id_token'],
    jwks_with_public_key,
    **jwt_kwargs)
```

#### Verify issued time
The `iat` value indicates what time the token was "issued at". We verify that this claim is valid by checking that the token was not issued in the future, with some leeway for clock skew.

```python
# tokens.py

# Validate 'iat' claim
plus_time_now_with_clock_skew = (datetime.utcnow() +
                                 timedelta(seconds=clock_skew))
plus_acceptable_iat = calendar.timegm(
    (plus_time_now_with_clock_skew).timetuple())

if 'iat' in claims and claims['iat'] > plus_acceptable_iat:
    return 'invalid iat claim', 401
```

#### Verify nonce
To mitigate replay attacks, verify that the `nonce` value in the `id_token` matches the `nonce` stored in the cookie `okta-oauth-nonce`.

```python
# tokens.py
if nonce != claims['nonce']:
    return 'invalid nonce', 401
```

### Set user session
If the `id_token` passes validation, we can then set the `user` session in our application.

In a production app, this code would lookup the `user` from a user store and set the session for that user. However, for simplicity, in this sample we set the session with the claims from the `id_token`.

```python
# views.py

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
```

### Logout
In django, you can clear the the user session by:

```python
# views.py

def logout_controller(request):
    # Log user out

    # Clear existing user
    user = User.objects.get(username=request.user).delete()
    logout(request)

    return redirect('/')
```

The Okta session is terminated in our client-side code.

## Conclusion
You have now successfully authenticated with Okta! Now what? With a user's `id_token`, you have basic claims into the user's identity. You can extend the set of claims by modifying the `response_type` and `scopes` to retrieve custom information about the user. This includes `locale`, `address`, `phone_number`, `groups`, and [more](http://developer.okta.com/docs/api/resources/oidc.html#scopes).

## Support

Have a question or see a bug? Email developers@okta.com. For feature requests, feel free to open an issue on this repo. If you find a security vulnerability, please follow our [Vulnerability Reporting Process](https://www.okta.com/vulnerability-reporting-policy/).

## License

Copyright 2017 Okta, Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
