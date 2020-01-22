import os
import base64
import json
from urllib.request import urlopen
from functools import wraps

from jose import jwt
from flask_restful import Resource, request
from models.base_model import db
from models.session_model import UserSession, UserSessionSchema
from models.contact_model import Contact
from flask_login import current_user, login_required, login_user
from flask import current_app 

# This function is VERY CRITICAL to the security of this application
# In particular, it needs to be sure to use a CSPRNG (cryptographically secure 
# pseudo-random number generator).
#
# More details here: https://www.hacksplaining.com/prevention/weak-session
def get_secure_random_id():
    return base64.b64encode(os.urandom(32)).decode('utf8')

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

AUTH0_DOMAIN = 'baltimore-corps.auth0.com'
ALGORITHMS = ["RS256"]

session_schema = UserSessionSchema()

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



class Session(Resource):
    @login_required
    def get(self):
        result = session_schema.dump(current_user)
        return {'status': 'success', 'data': result }, 200

    def post(self):
        config = current_app.config
        if config.get('TESTING'):
            assert config.get('DEPLOY_ENV') == 'test'
            return f(*args, **kwargs)

        token = get_token_auth_header()
        rsa_key = get_jwk(token)
        if not rsa_key:
            raise AuthError({"code": "invalid_header",
                            "description": "Unable to find appropriate key"}, 401)
        try:
            auth_payload = jwt.decode(
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

        print(auth_payload)
        account_id = auth_payload['sub']
        contact = Contact.query.filter_by(account_id=account_id).first()
        if not contact:
            return {'message': 'Contact does not exist for that account'}, 400

        user_session = UserSession(
            id=get_secure_random_id(),
            auth_id=auth_payload['sub'],
            contact_id=contact.id,
            jwt=token)
        login_user(user_session)
        db.session.add(user_session)
        db.session.commit()
        result = session_schema.dump(user_session)
        return {'status': 'success', 'data': result}, 201


