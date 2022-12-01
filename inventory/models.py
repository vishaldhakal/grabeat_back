from django.db import models
from api.models import DrinkItem
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    METRICES = (("Ml", "Ml"),)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    drinkk = models.ForeignKey(DrinkItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=500, default="Cash")
    quantity = models.IntegerField()
    metric = models.CharField(max_length=100, choices=METRICES, default="Ml")
    price = models.IntegerField()
    purchase_bill = models.FileField(blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.drinkk.name


class DrinksStock(models.Model):
    METRICES = (("Ml", "Ml"),)

    drinkk = models.ForeignKey(DrinkItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    metric = models.CharField(max_length=100, choices=METRICES, default="Ml")

    def __str__(self):
        return self.drinkk.name


@receiver(post_save, sender=DrinksPurchase)
def create_drink_stock(sender, instance=None, created=False, **kwargs):
    if created:
        drinkk2 = instance.drinkk
        check = DrinksStock.objects.filter(drinkk=drinkk2)
        if check.exists():
            newquantity = check[0].quantity
            newquantity += instance.quantity
            aaa = check[0]
            aaa.quantity = newquantity
            aaa.save()
        else:
            DrinksStock.objects.create(
                drinkk=instance.drinkk,
                quantity=instance.quantity,
                metric=instance.metric,
            )
