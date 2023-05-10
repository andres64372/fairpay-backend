import graphene
from rest_framework_simplejwt.tokens import RefreshToken

class RefreshType(graphene.ObjectType):
    access_token = graphene.String(required=True)
    refresh_token = graphene.String(required=True)

class RefreshMutation(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    refresh = graphene.Field(RefreshType)

    @classmethod
    def mutate(cls, root, info, token):
        refresh = RefreshToken(token)
        access = str(refresh.access_token)
        refresh = RefreshType(
            access_token=access,
            refresh_token=token,
        )
        return RefreshMutation(refresh=refresh)
        
        