from django.contrib import admin
from .models import FoodCategory, FoodItem, OrderItem, Order, Advertisement

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Advertisement)
