import graphene
from graphql_relay import from_global_id
from django.core.paginator import Paginator

from utils.authentication import jwt_authenticate_query
from models.models import (
    Account,
    AccountUser,
    Payment,
    UserPayment,
)

from schemas.account import (
    PaginatedAccountType,
    CreateAccountMutation,
    EditAccountMutation,
    DeleteAccountMutation,
)
from schemas.account_user import (
    PaginatedAccountUserType,
    CreateAccountUserMutation,
    EditAccountUserMutation,
    DeleteAccountUserMutation,
)
from schemas.payment import (
    PaginatedPaymentType,
    CreatePaymentMutation,
    EditPaymentMutation,
    DeletePaymentMutation,
)
from schemas.user_payment import (
    PaginatedUserPaymentType,
    CreateUserPaymentMutation,
    EditUserPaymentMutation,
    DeleteUserPaymentMutation,
)

from conf import settings


class Query(graphene.ObjectType):
    accounts = graphene.Field(
        PaginatedAccountType,
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=settings.DEFAULT_PAGE_ITEMS),
    )
    account_users = graphene.Field(
        PaginatedAccountUserType,
        account_id=graphene.String(required=True),
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=settings.DEFAULT_PAGE_ITEMS),
    )
    payments = graphene.Field(
        PaginatedPaymentType,
        account_id=graphene.String(required=True),
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=settings.DEFAULT_PAGE_ITEMS),
    )
    user_payments = graphene.Field(
        PaginatedUserPaymentType,
        payment_id=graphene.String(required=True),
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=settings.DEFAULT_PAGE_ITEMS),
    )

    @jwt_authenticate_query
    def resolve_accounts(
        root, 
        info, 
        page: int, 
        per_page: int
    ):
        paginator = Paginator(
            Account.objects.filter(user_id=info.context.user),
            per_page
        )
        return PaginatedAccountType(
            objects=paginator.page(page),
            total_pages=paginator.num_pages,
            current_page=page
        )

    @jwt_authenticate_query
    def resolve_account_users(
        root,
        _,
        account_id: str,
        page: int,
        per_page: int
    ):
        paginator = Paginator(
            AccountUser.objects.filter(
                account__pk=int(from_global_id(account_id).id)
            ),
            per_page
        )
        return PaginatedAccountUserType(
            objects=paginator.page(page),
            total_pages=paginator.num_pages,
            current_page=page
        )

    @jwt_authenticate_query
    def resolve_payments(
        root,
        _,
        account_id: str,
        page: int,
        per_page: int
    ):
        paginator = Paginator(
            Payment.objects.filter(
                account__pk=int(from_global_id(account_id).id)
            ),
            per_page
        )
        return PaginatedPaymentType(
            objects=paginator.page(page),
            total_pages=paginator.num_pages,
            current_page=page
        )

    @jwt_authenticate_query
    def resolve_user_payments(
        root,
        _,
        payment_id: str,
        page: int,
        per_page: int
    ):
        paginator = Paginator(
            UserPayment.objects.filter(
                payment__pk=int(from_global_id(payment_id).id)
            ),
            per_page
        )
        return PaginatedUserPaymentType(
            objects=paginator.page(page),
            total_pages=paginator.num_pages,
            current_page=page
        )


class Mutation(graphene.ObjectType):
    create_account = CreateAccountMutation.Field()
    edit_account = EditAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()
    create_user_account = CreateAccountUserMutation.Field()
    edit_user_account = EditAccountUserMutation.Field()
    delete_user_account = DeleteAccountUserMutation.Field()
    create_payment = CreatePaymentMutation.Field()
    edit_payment = EditPaymentMutation.Field()
    delete_payment = DeletePaymentMutation.Field()
    create_user_payment = CreateUserPaymentMutation.Field()
    edit_user_payment = EditUserPaymentMutation.Field()
    delete_user_payment = DeleteUserPaymentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
