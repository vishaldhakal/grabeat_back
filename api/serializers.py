from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):
    totals = serializers.SerializerMethodField()

    def get_totals(self, obj):
        return obj.ordertotal()

    class Meta:
        fields = "__all__"
        model = models.Order
        depth = 2


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True, read_only=True)()

    class Meta:
        fields = "__all__"
        model = models.Payment
        depth = 4


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Table
        depth = 1


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Vat
        depth = 1


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Tax
        depth = 1


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.FoodCategory
        depth = 1


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.FoodItem
        depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.OrderItem
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.User
        depth = 1
