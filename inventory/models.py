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
    METRICES = (
        ("Ml", "Ml"),
        ("Ltr", "Ltr"),
        ("Kg", "Kg"),
        ("mg", "mg"),
        ("Packets", "Packets"),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=500, default="Cash")
    quantity = models.FloatField()
    metric = models.CharField(max_length=100, default="Kg", choices=METRICES)
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
    METRICES = (
        ("Ml", "Ml"),
        ("Beer Bootles", "Beer Bootles"),
        ("Soft Drink Bottles [0.5 Ltr]", "Soft Drink Bottles [0.5 Ltr]"),
        ("Soft Drink Bottles [1 Ltr]", "Soft Drink Bottles [1 Ltr]"),
        ("Soft Drink Bottles [1.5 Ltr]", "Soft Drink Bottles [1.5 Ltr]"),
        ("Soft Drink Bottles [2 Ltr]", "Soft Drink Bottles [2 Ltr]"),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    drinkk = models.ForeignKey(DrinkItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=500, default="Cash")
    quantity = models.FloatField()
    metric = models.CharField(max_length=100, choices=METRICES, default="Ml")
    price = models.IntegerField()
    purchase_bill = models.FileField(blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.drinkk.name


class DrinksStock(models.Model):
    METRICES = (
        ("Ml", "Ml"),
        ("Beer Bootles", "Beer Bootles"),
        ("Beer Bootles", "Beer Bootles"),
    )

    drinkk = models.ForeignKey(DrinkItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    metric = models.CharField(max_length=100, choices=METRICES, default="Ml")

    def __str__(self):
        return self.drinkk.name


@receiver(post_save, sender=DrinksPurchase)
def create_drink_stock(sender, instance=None, created=False, **kwargs):
    if created:
        drinkk2 = instance.drinkk
        check = DrinksStock.objects.filter(drinkk=drinkk2)

        if check.exists():

            if instance.metric == "Soft Drink Bottles [0.5 Ltr]":
                add_qty = 500 * instance.quantity
            elif instance.metric == "Soft Drink Bottles [1 Ltr]":
                add_qty = 1000 * instance.quantity
            elif instance.metric == "Soft Drink Bottles [1.5 Ltr]":
                add_qty = 1500 * instance.quantity
            elif instance.metric == "Soft Drink Bottles [2 Ltr]":
                add_qty = 2000 * instance.quantity
            elif instance.metric == "Beer Bootles":
                add_qty = instance.quantity
            else:
                add_qty = instance.quantity

            newquantity = check[0].quantity
            newquantity += add_qty
            aaa = check[0]
            aaa.quantity = newquantity
            aaa.save()
        else:
            if instance.metric == "Ml" or instance.metric == "Beer Bootles":
                DrinksStock.objects.create(
                    drinkk=instance.drinkk,
                    quantity=instance.quantity,
                    metric=instance.metric,
                )
            else:
                qty = 1
                if instance.metric == "Soft Drink Bottles [0.5 Ltr]":
                    qty = 500
                elif instance.metric == "Soft Drink Bottles [1 Ltr]":
                    qty = 1000
                elif instance.metric == "Soft Drink Bottles [1.5 Ltr]":
                    qty = 1500
                else:
                    qty = 2000

                DrinksStock.objects.create(
                    drinkk=instance.drinkk,
                    quantity=qty * instance.quantity,
                    metric="Ml",
                )
