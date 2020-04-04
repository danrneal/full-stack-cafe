import json
from flask import request
from functools import wraps
from jose import jwt
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = 'full-stack-cafe.auth0.com'
ALGORITHMS = ['RS256']
API_IDENTIFIER = 'http://127.0.0.1/'


class AuthError(Exception):
    """Creates an exception to handle authorization errors

    Attributes:
        error: A dict containing information about the error
        status_code: An int representing the http status code
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the access token from the Authorization Header

    Returns:
        token: A str representing the auth token from the Authorization Header
    """

    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError(
            {
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected',
            }, 401
        )

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must start with Bearer',
            }, 401
        )
    elif len(parts) == 1:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Token not found',
            }, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must be Bearer token',
            }, 401
        )

    token = parts[1]

    return token


def verify_decode_jwt(token):
    """Decodes and verifies the validity of the provided access token

    Args:
        token: A str representing the access token to be decoded and verified

    Returns:
        payload: A dict representing the decoded and verified access token
    """

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': (
                    'Invalid header. Use an RS256 signed JWT Access Token'
                ),
            }, 401
        )

    if unverified_header['alg'] == 'HS256':
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': (
                    'Invalid header. Use an RS256 signed JWT Access Token'
                ),
            }, 401
        )

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
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
                    'code': 'token_expired',
                    'description': 'Token is expired',
                }, 401
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code': 'invalid_claims',
                    'description': (
                        'Incorrect claims, please check the audience and '
                        'issuer'
                    ),
                }, 401
            )
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token',
                }, 401
            )

        return payload

    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find appropriate key',
        }, 401
    )


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    raise Exception('Not Implemented')

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator