import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from models.models import Order

from views.middleware import jwt_authenticate_mutation

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node, )
        filter_fields = '__all__'

class CreateOrderMutation(graphene.Mutation):
    class Arguments:
        tip = graphene.Int()

    order = graphene.Field(OrderType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, tip = 0):
        order = Order.objects.create(user=info.context.user, tip=tip)
        return CreateOrderMutation(order=order)
        
        