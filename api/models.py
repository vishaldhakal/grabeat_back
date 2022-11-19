from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PAYMENT_STATUS = (
        ("Waiter", "Waiter"),
        ("Admin", "Admin"),
        ("Cashier", "Cashier"),
    )
    user_type = models.CharField(
        max_length=500, choices=PAYMENT_STATUS, default="Waiter"
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class FoodCategory(models.Model):
    name = models.CharField(max_length=900)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    thumbnail_image = models.FileField()
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_items = models.CharField(max_length=10, default=1)
    cart_status = models.CharField(max_length=500, default="Ordered")

    def __str__(self):
        return (
            self.no_of_items + " " + self.food_item.name + " by " + self.user.username
        )

    def totp(self):
        return (self.food_item.price) * (int(self.no_of_items))


class Order(models.Model):
    ORDER_STATUS = (
        ("Order Placed", "Order Placed"),
        ("Order Delivered", "Order Delivered"),
    )

    PAYMENT_STATUS = (
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_note = models.TextField()
    orderitems = models.ManyToManyField(OrderItem)
    status = models.CharField(
        max_length=400, choices=ORDER_STATUS, default="Order Placed"
    )
    orderdate = models.DateTimeField(auto_now_add=True, verbose_name="created")
    payment_status = models.CharField(
        max_length=500, choices=PAYMENT_STATUS, default="Unpaid"
    )
    payment_method = models.CharField(max_length=500)

    def ordertotal(self):
        total = 0
        for orderitemm in self.orderitems.all():
            total += orderitemm.totp()
        return total

    def __str__(self):
        return self.user.username + " Ordered " + self.status


class Vat(models.Model):
    vat_name = models.CharField(max_length=400)
    vat_percentage = models.IntegerField()

    def __str__(self):
        return self.vat_name


class Tax(models.Model):
    tax_name = models.CharField(max_length=400)
    tax_percentage = models.IntegerField()

    def __str__(self):
        return self.tax_name


class Table(models.Model):
    table_name = models.CharField(max_length=400)

    def __str__(self):
        return self.table_name
