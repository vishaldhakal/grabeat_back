from django.contrib import admin
from .models import (
    Supplier,
    Ingredient,
    Purchase,
    Stockout,
    DrinksPurchase,
    DrinksStock,
    Expenses,
)
from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg

admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Stockout)
admin.site.register(DrinksPurchase)
admin.site.register(Expenses)


@admin.register(Purchase)
class PurchaseAdmin(ModelAdminTotals, admin.ModelAdmin):
    list_totals = [("price", Sum)]
    list_display = (
        "supplier",
        "ingredient",
        "date",
        "payment_type",
        "quantity",
        "metric",
        "price",
        "remarks",
    )
    list_filter = (
        "date",
        "supplier__supplier_name",
        "ingredient__ingredient_name",
    )

    class Meta:
        model = Purchase


@admin.register(DrinksStock)
class DrinksStockAdmin(admin.ModelAdmin):
    list_display = (
        "drinkk",
        "quantity",
        "metric",
    )
    list_filter = ("drinkk__name",)

    class Meta:
        model = DrinksStock
