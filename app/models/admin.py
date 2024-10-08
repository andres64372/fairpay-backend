from django.contrib import admin
from .models import (
    Account,
    AccountUser,
    Payment,
    UserPayment,
)


class AccountAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
    pass


class AccountUserAdmin(admin.ModelAdmin):
    pass


class UserPaymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(AccountUser, AccountUserAdmin)
admin.site.register(UserPayment, UserPaymentAdmin)
