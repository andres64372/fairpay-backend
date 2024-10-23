import graphene
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene import relay
from graphql import GraphQLError

from models.models import (
    Account,
    AccountUser,
    Payment,
)
from utils.authentication import jwt_authenticate_mutation


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        interfaces = (relay.Node, )
        fields = (
            "description",
            "equal_accounts",
            "tax",
            "date"
        )
        filter_fields = {
            'description': ['exact', 'icontains', 'istartswith'],
        }


class PaginatedPaymentType(graphene.ObjectType):
    objects = graphene.List(PaymentType)
    total_pages = graphene.Int()
    current_page = graphene.Int()


class CreatePaymentMutation(graphene.Mutation):
    class Arguments:
        account_id = graphene.String(required=True)
        account_user_id = graphene.String(required=True)
        description = graphene.String(required=True)
        equal_accounts = graphene.Boolean(required=True)
        tax = graphene.Float(required=True)
        date = graphene.Date(required=True)

    payment = graphene.Field(PaymentType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        account_id,
        account_user_id,
        description,
        equal_accounts,
        tax,
        date,
    ):
        try:
            account = Account.objects.get(
                id=int(from_global_id(account_id).id))
            account_user = AccountUser.objects.get(
                id=int(from_global_id(account_user_id).id))
        except Account.DoesNotExist:
            raise GraphQLError("Account not found")
        except AccountUser.DoesNotExist:
            raise GraphQLError("User not found")
        if account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        payment = Payment.objects.create(
            description=description,
            equal_accounts=equal_accounts,
            tax=tax,
            date=date,
            account=account,
            account_user=account_user
        )
        return CreatePaymentMutation(payment=payment)


class EditPaymentMutation(graphene.Mutation):
    class Arguments:
        payment_id = graphene.ID(required=True)
        description = graphene.String()
        equal_accounts = graphene.Boolean()
        tax = graphene.Float()
        date = graphene.Date()

    payment = graphene.Field(PaymentType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        payment_id,
        description,
        equal_accounts,
        tax,
        date,
    ):
        try:
            payment = Payment.objects.get(
                id=int(from_global_id(payment_id).id))
        except Payment.DoesNotExist:
            raise GraphQLError("Payment not found")
        if payment.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        payment.description = (
            description
            if description is not None
            else payment.description
        )
        payment.equal_accounts = (
            equal_accounts
            if equal_accounts is not None
            else payment.equal_accounts
        )
        payment.tax = (
            tax
            if tax is not None
            else payment.tax
        )
        payment.date = (
            date
            if date is not None
            else payment.date
        )
        payment.save()
        return EditPaymentMutation(payment=payment)


class DeletePaymentMutation(graphene.Mutation):
    class Arguments:
        payment_id = graphene.ID(required=True)

    message = graphene.String()

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, payment_id):
        try:
            payment = Payment.objects.get(
                id=int(from_global_id(payment_id).id))
        except Payment.DoesNotExist:
            raise GraphQLError("Payment not found")
        if payment.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        payment.delete()
        return DeletePaymentMutation(message="deleted")
