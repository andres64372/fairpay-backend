import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginType(graphene.ObjectType):
    access_token = graphene.String(required=True)
    refresh_token = graphene.String(required=True)

class LoginMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    login = graphene.Field(LoginType)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            login = LoginType(
                access_token=refresh.access_token,
                refresh_token=refresh,
            )
            return LoginMutation(login=login)
        else:
            raise GraphQLError('Unauthorized')
        
        