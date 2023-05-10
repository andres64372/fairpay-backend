import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

class SignupType(graphene.ObjectType):
    access_token = graphene.String(required=True)
    refresh_token = graphene.String(required=True)

class SignupMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    signup = graphene.Field(SignupType)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = User.objects.create_user(username, username, password)
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            signup = SignupType(
                access_token=refresh.access_token,
                refresh_token=refresh,
            )
            return SignupMutation(signup=signup)
        else:
            raise GraphQLError('Unauthorized')