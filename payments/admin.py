from django.contrib import admin
from .models import Bank, PaymentMethod

admin.site.register(Bank)
admin.site.register(PaymentMethod)
