from django.db import models

from django.core.exceptions import ValidationError


class Account(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=60)
    
    @property
    def total(self):
        return sum([
            user_payment.amount * (100 + payment.tax) / 100
            for payment in Payment.objects.filter(account=self).prefetch_related('userpayment_set')
            for user_payment in payment.userpayment_set.all()
        ])
    
    def __str__(self) -> str:
        return self.name

class AccountUser(models.Model):
    name = models.CharField(max_length=30)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.account.name}"


class Payment(models.Model):
    description = models.CharField(max_length=30)
    equal_accounts = models.BooleanField()
    tax = models.FloatField()
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    @property
    def total(self):
        return sum([
            user_payment.amount * (100 + self.tax) / 100
            for user_payment in UserPayment.objects.filter(payment=self)
        ])

    def save(self, *args, **kwargs):
        if self.account_user.account != self.account:
            raise ValidationError("User not asociated with account")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.description} - {self.account.name}"


class UserPayment(models.Model):
    amount = models.FloatField()
    equal_accounts = models.BooleanField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    account_user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.account_user.name} - {self.payment.description}"
