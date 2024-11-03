import graphene
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene import relay
from graphql import GraphQLError

from models.models import (
    Account,
    AccountUser,
    Payment,
    UserPayment,
)
from schemas.user_payment import UserPaymentType
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
    
class QueryPaymentType(DjangoObjectType):
    total = graphene.Float()
    user_payments = graphene.List(UserPaymentType)

    class Meta:
        model = Payment
        interfaces = (relay.Node, )
        fields = (
            "account_user",
            "description",
            "equal_accounts",
            "tax",
            "date"
        )
        filter_fields = {
            'description': ['exact', 'icontains', 'istartswith'],
        }

    def resolve_total(self, _):
        return self.total
    
    def resolve_user_payments(self, _):
        return UserPayment.objects.filter(payment=self)

class PaginatedPaymentType(graphene.ObjectType):
    objects = graphene.List(QueryPaymentType)
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
        UserPayment.objects.bulk_create([
            UserPayment(
                amount=0,
                equal_accounts=False,
                payment=payment,
                account_user=account_user
            )
            for account_user in AccountUser.objects.filter(account=account)
        ])
        return CreatePaymentMutation(payment=payment)


class EditPaymentMutation(graphene.Mutation):
    class Arguments:
        payment_id = graphene.ID(required=True)
        account_user_id = graphene.String()
        description = graphene.String()
        equal_accounts = graphene.Boolean()
        tax = graphene.Float()
        date = graphene.Date()

    payment = graphene.Field(QueryPaymentType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(
        cls,
        _,
        info,
        payment_id,
        account_user_id,
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
        payment.account_user = (
            AccountUser.objects.get(
                id=int(from_global_id(account_user_id).id))
            if account_user_id is not None
            else payment.account_user
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
