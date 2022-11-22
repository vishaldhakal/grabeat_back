from django.contrib import admin
from .models import (
    FoodCategory,
    FoodItem,
    OrderItem,
    Order,
    User,
    Table,
    Tax,
    Vat,
    DrinkItem,
    Payment,
)

admin.site.register(FoodCategory)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Table)
admin.site.register(Tax)
admin.site.register(Vat)
admin.site.register(Payment)
""" admin.site.register(DrinkItem) """


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created", "updated")
    list_filter = ("created", "updated")

    class Meta:
        model = FoodItem
