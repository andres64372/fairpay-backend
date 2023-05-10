import graphene
from graphql import GraphQLError

from graphql_relay import from_global_id

from models.models import Order

from views.middleware import jwt_authenticate_mutation

class DeleteOrderType(graphene.ObjectType):
    status = graphene.Boolean(required=True)

class DeleteOrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order = graphene.Field(DeleteOrderType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, id):
        id = from_global_id(id)
        order = Order.objects.get(pk=id.id)
        if order.user == info.context.user and not order.closed:
            order.delete()
            return DeleteOrderMutation(order=DeleteOrderType(status=True))
        else:
            raise GraphQLError("Unauthorized")
        
        