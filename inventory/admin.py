from django.contrib import admin
from .models import Supplier, Ingredient, Purchase, Stockout, DrinksPurchase

admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Purchase)
admin.site.register(Stockout)
admin.site.register(DrinksPurchase)
