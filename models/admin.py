from django.contrib import admin

from models.models import *

@admin.register(Order)
class OrderArdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientArdmin(admin.ModelAdmin):
    pass