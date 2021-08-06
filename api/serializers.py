from rest_framework import serializers
from . import models


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


class OrderSerializer(serializers.ModelSerializer):
    totals = serializers.SerializerMethodField()

    def get_totals(self, obj):
        return obj.ordertotal()

    class Meta:
        fields = "__all__"
        model = models.Order
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.User
        depth = 1
