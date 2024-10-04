import jwt

import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from app.configs import oauthSettings, MS_JWT_KEYS
from app.configs.oauth.xbox import MicrosoftJWTKey
from app.exceptions.auth import InvalidAuthorizationToken

__all__ = (
    "validate_jwt",
    "read_jwt_payload",
    "is_jwt_valid",
)


def ensure_bytes(key):
    if isinstance(key, str):
        key = key.encode("utf-8")
    return key


def decode_value(val):
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
    return int.from_bytes(decoded, "big")


def rsa_pem_from_jwk(jwk: MicrosoftJWTKey):
    return (
        RSAPublicNumbers(n=decode_value(jwk.n), e=decode_value(jwk.e))
        .public_key(default_backend())
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken("missing headers")
    try:
        return headers["kid"]
    except KeyError:
        raise InvalidAuthorizationToken("missing kid")


def get_jwk(kid) -> MicrosoftJWTKey:
    if jwk := MS_JWT_KEYS.get(kid):
        return jwk
    raise InvalidAuthorizationToken("kid not recognized")


def get_public_key(token):
    _jwk = get_jwk(get_kid(token))
    return rsa_pem_from_jwk(_jwk)


def validate_jwt(jwt_to_validate):
    """
    return None or throws Execption if JWT is not valid
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
    except Exception as ex:
        print("The JWT is not valid!")
    else:
        print("The JWT is valid!")


def read_jwt_payload(jwt_to_validate) -> dict | None:
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
        # TODO: handle exception
        print(f"{ex=}")
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
