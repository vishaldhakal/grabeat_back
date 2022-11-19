from django.contrib import admin
from .models import FoodCategory, FoodItem, OrderItem, Order, User, Table, Tax, Vat

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Table)
admin.site.register(Tax)
admin.site.register(Vat)
