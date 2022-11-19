from django.contrib import admin
from .models import Supplier,Ingredient,Purchase,Stockout

admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Purchase)
admin.site.register(Stockout)
