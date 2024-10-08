import graphene
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene import relay
from graphql import GraphQLError

from models.models import (
    Account,
    AccountUser,
)
from utils.authentication import jwt_authenticate_mutation


class AccountUserType(DjangoObjectType):
    class Meta:
        model = AccountUser
        interfaces = (relay.Node, )
        fields = ("name",)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class PaginatedAccountUserType(graphene.ObjectType):
    objects = graphene.List(AccountUserType)
    total_pages = graphene.Int()
    current_page = graphene.Int()


class CreateAccountUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        account_id = graphene.ID()

    account_user = graphene.Field(AccountUserType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, _, info, name, account_id):
        try:
            account = Account.objects.get(
                id=int(from_global_id(account_id).id))
        except Account.DoesNotExist:
            raise GraphQLError("Account not found")
        if account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        account_user = AccountUser.objects.create(
            name=name,
            account=account
        )
        return CreateAccountUserMutation(account_user=account_user)


class EditAccountUserMutation(graphene.Mutation):
    class Arguments:
        account_user_id = graphene.ID()
        name = graphene.String()

    account_user = graphene.Field(AccountUserType)

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, _, info, account_user_id, name):
        try:
            account_user = AccountUser.objects.get(
                id=int(from_global_id(account_user_id).id))
        except AccountUser.DoesNotExist:
            raise GraphQLError("User not found")
        if account_user.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        account_user.name = name if name is not None else account_user.name
        account_user.save()
        return EditAccountUserMutation(account_user=account_user)


class DeleteAccountUserMutation(graphene.Mutation):
    class Arguments:
        account_user_id = graphene.ID(required=True)

    message = graphene.String()

    @classmethod
    @jwt_authenticate_mutation
    def mutate(cls, _, info, account_id):
        try:
            account_user = AccountUser.objects.get(
                id=int(from_global_id(account_id).id))
        except AccountUser.DoesNotExist:
            raise GraphQLError("User not found")
        if account_user.account.user_id != info.context.user:
            raise GraphQLError("Unauthorized")
        account_user.delete()
        return DeleteAccountUserMutation(message="deleted")
