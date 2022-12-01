from rest_framework import serializers
from . import models


class DrinkPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.DrinksPurchase
        depth = 1


class DrinkStockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.DrinksStock
        depth = 1


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Purchase
        depth = 1
