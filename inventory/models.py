from django.db import models
from api.models import DrinkItem, FoodItem
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


class Expenses(models.Model):
    expense_title = models.CharField(max_length=500)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.expense_title


class DrinksPurchase(models.Model):
    METRICES = (
        ("Ml", "Ml"),
        ("Beer Bottles", "Beer Bottles"),
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
        ("Beer Bottles", "Beer Bottles"),
    )

    drinkk = models.ForeignKey(DrinkItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    metric = models.CharField(max_length=100, choices=METRICES, default="Ml")

    def __str__(self):
        return self.drinkk.name


@receiver(post_save, sender=FoodItem)
def create_drink(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_a_drink:
            check = DrinkItem.objects.filter(name=instance.name)
            if check.exists():
                vv = check[0]
                check = DrinksStock.objects.filter(drinkk=vv)
                if check.exists():
                    pass
                else:
                    if vv.type_of_drink == "Beer":
                        DrinksStock.objects.create(
                            drinkk=vv,
                            quantity=0,
                            metric="Ml",
                        )
                    else:
                        DrinksStock.objects.create(
                            drinkk=vv,
                            quantity=0,
                            metric="Ml",
                        )
            else:
                DrinkItem.objects.create(
                    name=instance.name,
                    thumbnail_image=instance.thumbnail_image,
                    type_of_drink=instance.type_of_drink,
                )

                vv = DrinkItem.objects.get(name=instance.name)
                check = DrinksStock.objects.filter(drinkk=vv)
                if check.exists():
                    pass
                else:
                    if vv.type_of_drink == "Beer":
                        DrinksStock.objects.create(
                            drinkk=vv,
                            quantity=0,
                            metric="Beer Bottles",
                        )
                    else:
                        DrinksStock.objects.create(
                            drinkk=vv,
                            quantity=0,
                            metric="Ml",
                        )


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
            elif instance.metric == "Beer Bottles":
                add_qty = instance.quantity
            else:
                add_qty = instance.quantity

            newquantity = check[0].quantity
            newquantity += add_qty
            aaa = check[0]
            aaa.quantity = newquantity
            aaa.save()
        else:
            if instance.metric == "Ml" or instance.metric == "Beer Bottles":
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
