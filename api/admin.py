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
    CanclePayment,
)
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg

admin.site.register(FoodCategory)
admin.site.register(User)
admin.site.register(Table)
admin.site.register(Tax)
admin.site.register(Vat)
admin.site.register(DrinkItem)
admin.site.register(CanclePayment)
""" admin.site.register(DrinkItem) """


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


@admin.register(Payment)
class PaymentAdmin(ImportExportActionModelAdmin, ModelAdminTotals, admin.ModelAdmin):
    list_display = (
        "user",
        "created",
        "updated",
        "discount_type",
        "discount_percentage",
        "discount",
        "payment_method",
        "amount_paidd",
        "bank_name",
        "table",
    )
    list_filter = (
        "created",
        "updated",
        "table__table_name",
        "user__username",
        "payment_method__payment_method_name",
    )
    resource_class = PaymentResource
    list_totals = [("discount", Sum), ("amount_paidd", Sum)]

    class Meta:
        model = Payment


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created",
        "updated",
        "food_item",
        "no_of_items",
        "Price_Each",
        "Total_Price",
    )
    list_filter = (
        "created",
        "updated",
        "food_item",
    )

    class Meta:
        model = OrderItem


class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = (
        "__str__",
        "table",
        "created",
        "updated",
        "status",
        "order_note",
        "Order_Items",
        "Order_Total",
    )
    list_filter = ("created", "updated", "table", "user")


admin.site.register(Order, OrderAdmin)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created", "updated")
    list_filter = ("created", "updated")

    class Meta:
        model = FoodItem
