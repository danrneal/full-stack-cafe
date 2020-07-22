"""Logic for authenticating users and verifying permissions for a request.

Attributes:
    AUTH0_DOMAIN: A str representing the domain for the Auth0 app
    ALGORITHMS: A list representing the accepted encryption algorithms for the
        access token
    API_IDENTIFIER: A str representing the unique identifier for the Auth0 api

Classes:
    AuthError()
"""

import json
from functools import wraps

from flask import request
from jose import jwt
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = "full-stack-cafe.auth0.com"
ALGORITHMS = ["RS256"]
API_IDENTIFIER = "http://127.0.0.1/"


class AuthError(Exception):
    """Creates an exception to handle authorization errors.

    Attributes:
        error: A dict containing information about the error
        status_code: An int representing the http status code
    """

    def __init__(self, error, status_code):
        """Set-up for AuthError Exception."""
        super().__init__()
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the access token from the Authorization Header.

    Returns:
        token: A str representing the auth token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)

    if not auth:
        raise AuthError(
            {
                "error_code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "error_code": "invalid_header",
                "description": "Authorization header must start with Bearer",
            },
            401,
        )
    if len(parts) == 1:
        raise AuthError(
            {
                "error_code": "invalid_header",
                "description": "Token not found",
            },
            401,
        )
    if len(parts) > 2:
        raise AuthError(
            {
                "error_code": "invalid_header",
                "description": "Authorization header must be Bearer token",
            },
            401,
        )

    token = parts[1]

    return token


def get_token_rsa_key(token):
    """Retrieves the rsa key of the provided access token.

    Args:
        token: A str representing the access token to retrieve the rsa key for

    Returns:
        rsa_key: A dict representing the rsa key for the the given token
    """
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError(
            {
                "error_code": "invalid_header",
                "description": (
                    "Invalid header. Use an RS256 signed JWT Access Token"
                ),
            },
            401,
        )

    if unverified_header["alg"] == "HS256":
        raise AuthError(
            {
                "error_code": "invalid_header",
                "description": (
                    "Invalid header. Use an RS256 signed JWT Access Token"
                ),
            },
            401,
        )

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f'https://{AUTH0_DOMAIN}/',
            )
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'error_code': 'token_expired',
                    'description': 'Token is expired',
                }, 401
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'error_code': 'invalid_claims',
                    'description': (
                        'Incorrect claims, please check the audience and '
                        'issuer'
                    ),
                }, 401
            )
        except Exception:
            raise AuthError(
                {
                    'error_code': 'invalid_header',
                    'description': 'Unable to parse authentication token',
                }, 401
            )

        return payload

    raise AuthError(
        {
            'error_code': 'invalid_header',
            'description': 'Unable to find appropriate key',
        }, 401
    )


def check_permissions(permission, payload):
    """Checks if a decoded access token contains the required peermission.

    Args:
        permission: A str representing the required permission
        payload: A dict representing the decoded access token
    """
    permissions = payload.get("permissions")

    if permissions is None:
        raise AuthError(
            {
                "error_code": "invalid_claims",
                "description": (
                    "Incorrect claims, please check the role-based access "
                    "control settings"
                ),
            },
            401,
        )

    if permission not in permissions:
        raise AuthError(
            {
                "error_code": "forbidden",
                "description": (
                    "You are not authorized to access this resource"
                ),
            },
            403,
        )


def requires_auth(permission=""):
    """A decorator to authenticate users and verify permissions for a request.

    Args:
        permission: A str representing the permission required to access the
            requested resource
    """

    def requires_auth_decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
