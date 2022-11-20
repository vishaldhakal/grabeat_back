from django.db import models


class Bank(models.Model):
    bank_name = models.CharField(max_length=500)

    def __str__(self):
        return self.bank_name


class PaymentMethod(models.Model):
    payment_method_name = models.CharField(max_length=500)

    def __str__(self):
        return self.payment_method_name
