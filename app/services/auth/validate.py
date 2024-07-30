import jwt

import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from pprint import pprint
from app.configs import oauthSettings


def ensure_bytes(key):
    if isinstance(key, str):
        key = key.encode("utf-8")
    return key


def decode_value(val):
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
    return int.from_bytes(decoded, "big")


def rsa_pem_from_jwk(jwk):
    return (
        RSAPublicNumbers(n=decode_value(jwk["n"]), e=decode_value(jwk["e"]))
        .public_key(default_backend())
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )



class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__("Invalid authorization token: " + details)


def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken("missing headers")
    try:
        return headers["kid"]
    except KeyError:
        raise InvalidAuthorizationToken("missing kid")


def get_jwk(kid):
    for jwk in jwks.get("keys"):
        if jwk.get("kid") == kid:
            return jwk
    raise InvalidAuthorizationToken("kid not recognized")


def get_public_key(token):
    return rsa_pem_from_jwk(get_jwk(get_kid(token)))


def validate_jwt(jwt_to_validate):
    try:

        public_key = get_public_key(jwt_to_validate)
        decoded = jwt.decode(
            jwt_to_validate,
            public_key,
            verify=True,
            algorithms=oauthSettings.xbox.OAUTH_ALGORITHMS,
            audience=oauthSettings.xbox.OAUTH_AUDIENCE,
            issuer=oauthSettings.xbox.TOKEN_ISSUER,
        )
    except Exception as ex:
        print("The JWT is not valid!")
    else:
        print("The JWT is valid!")


def read_jwt(jwt_to_validate) -> dict | None:
    """
    if valid -> object
    if not valid -> None
    """
    try:
        public_key = get_public_key(jwt_to_validate)
        decoded = jwt.decode(
            jwt_to_validate,
            public_key,
            verify=True,
            algorithms=oauthSettings.xbox.OAUTH_ALGORITHMS,
            audience=oauthSettings.xbox.OAUTH_AUDIENCE,
            issuer=oauthSettings.xbox.TOKEN_ISSUER,
        )
        return decoded
    except Exception as ex:
        # print("The JWT is not valid!")
        return


def is_jwt_valid(jwt_to_validate: str) -> bool:
    public_key = None
    try:
        public_key = get_public_key(jwt_to_validate)
    except:
        # Error on public key decrypt
        return False
    try:
        jwt.decode(
            jwt_to_validate,
            public_key,
            verify=True,
            algorithms=oauthSettings.xbox.OAUTH_ALGORITHMS,
            audience=oauthSettings.xbox.OAUTH_AUDIENCE,
            issuer=oauthSettings.xbox.TOKEN_ISSUER,
        )
    except Exception as ex:
        return False
    return True
