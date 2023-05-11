from rest_framework_simplejwt.authentication import JWTAuthentication
from graphql import GraphQLError

def jwt_authenticate_query(resolve_func):
    def wrapper(parent, info, **kwargs):
        request = info.context
        user = JWTAuthentication().authenticate(request)
        if user:
            request.user = user[0]
        else:
            raise GraphQLError('Invalid Token')
        return resolve_func(parent, info, **kwargs)
    return wrapper

def jwt_authenticate_mutation(resolve_func):
    def wrapper(cls, parent, info, **kwargs):
        request = info.context
        user = JWTAuthentication().authenticate(request)
        if user:
            request.user = user[0]
        else:
            raise GraphQLError('Invalid Token')
        return resolve_func(cls, parent, info, **kwargs)
    return wrapper