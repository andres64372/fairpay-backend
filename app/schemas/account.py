import graphene
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene import relay
from graphql import GraphQLError

from models.models import Account
from utils.authentication import jwt_authenticate_mutation


class AccountType(DjangoObjectType):
    class Meta:
        model = Account
        interfaces = (relay.Node, )
        fields = ("name", "user_id")
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class PaginatedAccountType(graphene.ObjectType):
    objects = graphene.List(AccountType)
    total_pages = graphene.Int()
    current_page = graphene.Int()


class CreateAccountMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    account = graphene.Field(AccountType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, name):
        account = Account.objects.create(
            name=name,
            user_id=info.context.user,
        )
        return CreateAccountMutation(account=account)


class EditAccountMutation(graphene.Mutation):
    class Arguments:
        account_id = graphene.ID(required=True)
        name = graphene.String()

    account = graphene.Field(AccountType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, account_id, name):
        try:
            account = Account.objects.get(
                id=int(from_global_id(account_id).id))
        except Account.DoesNotExist:
            raise GraphQLError("Account not found")
        if account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        account.name = name if name is not None else account.name
        account.save()
        return EditAccountMutation(account=account)


class DeleteAccountMutation(graphene.Mutation):
    class Arguments:
        account_id = graphene.ID(required=True)

    message = graphene.String()

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, root, info, account_id):
        try:
            account = Account.objects.get(
                id=int(from_global_id(account_id).id))
        except Account.DoesNotExist:
            raise GraphQLError("Account not found")
        if account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        account.delete()
        return DeleteAccountMutation(message="deleted")
