import os
import json
import base64
import time
from urllib.request import urlopen
from functools import wraps
from datetime import datetime, timedelta
from flask_login import current_user

from flask import current_app, request
from jose import jwt

from models.base_model import db
from models.session_model import UserSession

AUTH0_DOMAIN = 'baltimore-corps.auth0.com'
ALGORITHMS = ["RS256"]

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

TEST_KEY = {
    "kty": "RSA",
    "kid": "test_key",
    "use": "sig",
    "e": "AQAB",
    "n": "xUI0GGpnrJOayEn0Vlsit1FcaYN1dKTgfGA6FzYEqZgJM-c7Qi7Qes03S7UjZfY1_UhH1_Y_LKSm2IinE0c0GcjFPpFgraxF3YhiGzNFGRIzPr7rXYowfC1mUrSL25O1q0_xntEjr8r3z-6yrArdsZdlu7Z3lpsbnEe88wSfBhFdJmhXaA93yMmvAm9T8yWPnLLgRtkoVTpQi_wCq4tX-igXbYeDCG4vOIv-goxrg9KYJS-mE_nAsib0pTlOkQsHhPE3FZNOubl6Awk_nmwrYleCz2yWDp6t3w4peyNYkldAwmn4Dpw-vfZre7ptOAoLluco0swZxYyGhjegh5AFRw"
}

TEST_JWT = {
  "iss": "https://baltimore-corps.auth0.com/",
  "aud": [
    "test",
  ],
  "iat": int(time.time()),
  "exp": int(time.time()) + 86400,
  "scope": "openid profile email",
  "permissions": []
}

def get_jwk(token):
    if current_app.config.get('TESTING'):
        assert current_app.config.get('DEPLOY_ENV') == 'test'
        return TEST_KEY

    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    return rsa_key

def validate_jwt(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        config = current_app.config
        # TODO: Replace this with actual auth testbed in tests
        if config.get('TESTING'):
            assert config.get('DEPLOY_ENV') == 'test'
            token = get_token_auth_header()
            if token.startswith('test-valid|'):
                test_jwt = TEST_JWT.copy()
                test_jwt['sub'] = token
                request._get_current_object().jwt = test_jwt
            else:
                raise AuthError({"code": "token_test_invalid",
                                "description": "test token is invalid"}, 401)
            return f(*args, **kwargs)

        token = get_token_auth_header()
        rsa_key = get_jwk(token)
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=config['AUTH0_API_AUDIENCE'],
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            request._get_current_object().jwt = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


# This function is VERY CRITICAL to the security of this application
# In particular, it needs to be sure to use a CSPRNG (cryptographically secure 
# pseudo-random number generator).
#
# More details here: https://www.hacksplaining.com/prevention/weak-session
def get_secure_random_id():
    return base64.b64encode(os.urandom(32)).decode('utf8')

# 3 hour seessions
SESSION_DURATION = timedelta(hours=3)

def create_session(contact_id, jwt_payload):
    account_id = jwt_payload['sub']

    user_session = UserSession(
        id=get_secure_random_id(),
        auth_id=account_id,
        contact_id=contact_id,
        jwt=json.dumps(jwt_payload),
        expiration=datetime.utcnow() + SESSION_DURATION,
    )

    db.session.add(user_session)
    db.session.commit()

    return user_session

def refresh_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user.expiration = datetime.utcnow() + SESSION_DURATION
        db.session.commit()
        return f(*args, **kwargs)
    return decorated

def delete_session(user_session):
    db.session.delete(user_session)
    db.session.commit()

def get_current_user_permissions():
    payload = json.loads(current_user.jwt)
    return payload.get('permissions', [])

def has_permission(permission):
    permissions = get_current_user_permissions()
    print(permissions, permission)
    return permission in permissions

def is_authorized_with_permission(permission):
    if current_app.config.get('TESTING'):
        assert current_app.config.get('DEPLOY_ENV') == 'test'
        return True
    
    return has_permission(permission)

def is_authorized_view(contact_id):
    return is_authorized(contact_id, 'view')

def is_authorized_write(contact_id):
    return is_authorized(contact_id, 'write')

def is_authorized(contact_id, operation):
    if current_app.config.get('TESTING'):
        assert current_app.config.get('DEPLOY_ENV') == 'test'
        return True

    if has_permission(f'{operation}:all-users'):
        return True

    return contact_id == current_user.contact_id



def unauthorized():
    return ({'message': 'You are not authorized to access this endpoint'}, 401)
