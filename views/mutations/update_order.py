import graphene
from graphql import GraphQLError
from graphene import relay
from graphene_django import DjangoObjectType

from graphql_relay import from_global_id

from models.models import Order

from views.middleware import jwt_authenticate_mutation

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node, )
        filter_fields = '__all__'

class UpdateOrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tip = graphene.Int()
        name = graphene.String()
        closed = graphene.Boolean()

    order = graphene.Field(OrderType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, id, name = None, tip = None, closed = None):
        id = from_global_id(id)
        order = Order.objects.get(pk=id.id)
        if order.user == info.context.user:
            order.name = name if name is not None else order.name
            order.tip = tip if tip is not None else order.tip
            order.closed = closed if closed is not None else order.closed
            order.save()
            return UpdateOrderMutation(order)
        else:
            raise GraphQLError('Unauthorized')        
        