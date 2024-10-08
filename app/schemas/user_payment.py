import graphene
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene import relay
from graphql import GraphQLError

from models.models import (
    Payment,
    UserPayment,
)
from utils.authentication import jwt_authenticate_mutation


class UserPaymentType(DjangoObjectType):
    class Meta:
        model = UserPayment
        interfaces = (relay.Node, )
        fields = (
            "amount",
            "equal_accounts",
        )


class PaginatedUserPaymentType(graphene.ObjectType):
    objects = graphene.List(UserPaymentType)
    total_pages = graphene.Int()
    current_page = graphene.Int()


class CreateUserPaymentMutation(graphene.Mutation):
    class Arguments:
        payment_id = graphene.String(required=True)
        amount = graphene.Float(required=True)
        equal_accounts = graphene.Boolean(required=True)

    user_payment = graphene.Field(UserPaymentType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        payment_id,
        amount,
        equal_accounts,

    ):
        try:
            payment = Payment.objects.get(
                id=int(from_global_id(payment_id).id))
        except Payment.DoesNotExist:
            raise GraphQLError("Payment not found")
        if payment.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        user_payment = UserPayment.objects.create(
            amount=amount,
            equal_accounts=equal_accounts,
        )
        return CreateUserPaymentMutation(user_payment=user_payment)


class EditUserPaymentMutation(graphene.Mutation):
    class Arguments:
        user_payment_id = graphene.String(required=True)
        amount = graphene.Float(required=True)
        equal_accounts = graphene.Boolean(required=True)

    user_payment = graphene.Field(UserPaymentType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        user_payment_id,
        amount,
        equal_accounts,

    ):
        try:
            user_payment = UserPayment.objects.get(
                id=int(from_global_id(user_payment_id).id))
        except Payment.DoesNotExist:
            raise GraphQLError("Payment not found")
        if user_payment.payment.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        user_payment.amount = (
            amount
            if amount is not None
            else user_payment.amount
        )
        user_payment.equal_accounts = (
            equal_accounts
            if equal_accounts is not None
            else user_payment.equal_accounts
        )
        return EditUserPaymentMutation(user_payment=user_payment)


class DeleteUserPaymentMutation(graphene.Mutation):
    class Arguments:
        user_payment_id = graphene.String(required=True)

    message = graphene.String()

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        user_payment_id,
    ):
        try:
            user_payment = UserPayment.objects.get(
                id=int(from_global_id(user_payment_id).id))
        except UserPayment.DoesNotExist:
            raise GraphQLError("User not found")
        if user_payment.payment.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        user_payment.delete()
        return DeleteUserPaymentMutation(message="deleted")
