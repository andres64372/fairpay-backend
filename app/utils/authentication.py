import urllib
import json

import jwt
from jwt.algorithms import RSAAlgorithm
from graphql import GraphQLError
from conf import settings


class JWT:
    def __init__(self, token):
        self.__token = token

    def get_jwks(self):
        with urllib.request.urlopen(
            f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        ) as url:
            return json.load(url)

    def get_public_key(self, jwk, jwt_header):
        rsa_key = {}
        if jwk["kid"] == jwt_header["kid"]:
            rsa_key = {
                "kty": jwk["kty"],
                "kid": jwk["kid"],
                "use": jwk["use"],
                "n": jwk["n"],
                "e": jwk["e"]
            }
        return rsa_key

    def validate_jwt(self) -> str:
        jwks = self.get_jwks()["keys"]
        unverified_header = jwt.get_unverified_header(self.__token)

        rsa_key = {}
        for jwk in jwks:
            rsa_key = self.get_public_key(jwk, unverified_header)
            if rsa_key:
                break

        if not rsa_key:
            raise ValueError("No appropriate key found")

        payload = jwt.decode(
            self.__token,
            RSAAlgorithm.from_jwk(rsa_key),
            algorithms=['RS256'],
            audience=[f'https://{settings.AUTH0_DOMAIN}/api/v2/', settings.AUTH0_CLIENT],
            issuer=f'https://{settings.AUTH0_DOMAIN}/',
        )

        return payload['sub']


def jwt_authenticate_query(resolve_func):
    def wrapper(parent, info, **kwargs):
        request = info.context
        if settings.DEBUG:
            request.user = 'default'
        else:
            auth = request.META.get('HTTP_AUTHORIZATION')
            if auth:
                token = JWT(auth[7:])
                request.user = token.validate_jwt()
            else:
                raise GraphQLError('Invalid Token')
        return resolve_func(parent, info, **kwargs)
    return wrapper


def jwt_authenticate_mutation(resolve_func):
    def wrapper(cls, parent, info, **kwargs):
        request = info.context
        if settings.DEBUG:
            request.user = 'default'
        else:
            auth = request.META.get('HTTP_AUTHORIZATION')
            if auth:
                token = JWT(auth[7:])
                request.user = token.validate_jwt()
            else:
                raise GraphQLError('Invalid Token')
        request.user = 'default'
        return resolve_func(cls, parent, info, **kwargs)
    return wrapper
