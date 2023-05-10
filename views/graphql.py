import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from graphql import GraphQLError
from graphql_relay import from_global_id

from models.models import *

from .mutations.signup import SignupMutation
from .mutations.login import LoginMutation
from .mutations.refresh import RefreshMutation
from .mutations.create_order import CreateOrderMutation
from .mutations.update_order import UpdateOrderMutation
from .mutations.create_client import CreateClientMutation
from .mutations.update_client import UpdateClientMutation
from .mutations.delete_order import DeleteOrderMutation
from .mutations.delete_client import DeleteClientMutation

from .middleware import jwt_authenticate_query

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node, )
        filter_fields = {
            'created': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'tip': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'closed': ['exact']
        }

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        interfaces = (relay.Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'amount': ['exact', 'gt', 'gte', 'lt', 'lte']
        }

class Query(graphene.ObjectType):
    order = graphene.Field(OrderType, id=graphene.ID(required=True))
    all_orders = DjangoFilterConnectionField(OrderType)

    @jwt_authenticate_query
    def resolve_order(self, info, id):
        id = from_global_id(id)
        order = Order.objects.get(pk=id.id)
        if order.user == info.context.user:
            return order
        else:
            raise GraphQLError('Unauthorized')

    @jwt_authenticate_query
    def resolve_all_orders(self, info):
        return Order.objects.filter(user=info.context.user)
    
    client = relay.Node.Field(ClientType)

    @jwt_authenticate_query
    def resolve_client(self, info, id):
        id = from_global_id(id)
        client = Client.objects.get(pk=id.id)
        if client.order.user == info.context.user:
            return client
        else:
            raise GraphQLError('Unauthorized')

class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    signup = SignupMutation.Field()
    refresh = RefreshMutation.Field()
    create_order = CreateOrderMutation.Field()
    update_order = UpdateOrderMutation.Field()
    create_client = CreateClientMutation.Field()
    update_client = UpdateClientMutation.Field()
    delete_order = DeleteOrderMutation.Field()
    delete_client = DeleteClientMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)