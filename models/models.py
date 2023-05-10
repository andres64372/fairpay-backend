from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    tip = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.created.strftime('%Y-%m-%d %H:%M')

class Client(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name