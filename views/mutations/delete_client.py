import graphene
from graphql import GraphQLError

from graphql_relay import from_global_id

from models.models import Client

from views.middleware import jwt_authenticate_mutation

class DeleteClientType(graphene.ObjectType):
    status = graphene.Boolean(required=True)

class DeleteClientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    client = graphene.Field(DeleteClientType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, id):
        id = from_global_id(id)
        client = Client.objects.get(pk=id.id)
        if client.order.user == info.context.user:
            client.delete()
            return DeleteClientMutation(client=DeleteClientType(status=True))
        else:
            raise GraphQLError("Unauthorized")
        
        