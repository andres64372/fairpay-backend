import graphene
from graphql import GraphQLError
from graphene import relay
from graphene_django import DjangoObjectType

from graphql_relay import from_global_id

from models.models import Client, Order

from views.middleware import jwt_authenticate_mutation

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        interfaces = (relay.Node, )
        filter_fields = '__all__'

class CreateClientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        amount = graphene.Float()

    client = graphene.Field(ClientType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, id, name, amount):
        id = from_global_id(id)
        order = Order.objects.get(pk=id.id)
        if not order.closed:
            client = Client.objects.create(
                order=order,
                name=name,
                amount=amount,
            )
            return CreateClientMutation(client=client)
        else:
            raise GraphQLError("Unauthorized")

        
        