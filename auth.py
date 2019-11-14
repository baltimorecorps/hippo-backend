import json
from urllib.request import urlopen
from functools import wraps

from flask import current_app, request, _request_ctx_stack
from jose import jwt

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

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        config = current_app.config
        # TODO: Replace this with actual auth testbed in tests
        if config.get('TESTING'):
            assert config.get('DEPLOY_ENV') == 'test'
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

            _request_ctx_stack.top.current_user = payload
            # Not sure why the above doesn't work, but this does
            request._get_current_object().current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated
