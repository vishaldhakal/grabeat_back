from django.db import models
from api.models import FoodItem


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=500)
    contact_number = models.CharField(max_length=500)

    def __str__(self):
        return self.supplier_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=500)

    def __str__(self):
        return self.ingredient_name


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=500, default="Cash")
    quantity = models.IntegerField()
    metric = models.CharField(max_length=100)
    price = models.IntegerField()
    purchase_bill = models.FileField(blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.ingredient.ingredient_name


class Stockout(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    metric = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.ingredient.ingredient_name


class DrinksPurchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    drinkk = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=500, default="Cash")
    quantity = models.IntegerField()
    metric = models.CharField(max_length=100)
    price = models.IntegerField()
    purchase_bill = models.FileField(blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.drinkk
