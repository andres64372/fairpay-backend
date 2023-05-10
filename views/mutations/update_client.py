import graphene
from graphql import GraphQLError
from graphene import relay
from graphene_django import DjangoObjectType

from graphql_relay import from_global_id

from models.models import Client

from views.middleware import jwt_authenticate_mutation

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        interfaces = (relay.Node, )
        filter_fields = '__all__'

class UpdateClientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        amount = graphene.Float()

    client = graphene.Field(ClientType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, id, name = None, amount = None):
        id = from_global_id(id)
        client = Client.objects.get(pk=id.id)
        if client.order.user == info.context.user and not client.order.closed:
            client.name = name if name is not None else client.name
            client.amount = amount if amount is not None else client.amount
            client.save()
            return UpdateClientMutation(client)
        else:
            raise GraphQLError('Unauthorized')
        
        