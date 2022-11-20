from rest_framework import serializers
from . import models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Bank
        depth = 1


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.PaymentMethod
        depth = 1
