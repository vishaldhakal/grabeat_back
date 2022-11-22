from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from payments.models import PaymentMethod, Bank


class Table(models.Model):
    table_name = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.table_name


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
    category = models.ManyToManyField(FoodCategory)
    name = models.CharField(max_length=500)
    thumbnail_image = models.FileField()
    price = models.IntegerField()
    is_a_drink = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DrinkItem(models.Model):
    name = models.CharField(max_length=500)
    thumbnail_image = models.FileField()
    is_a_drink = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.name


@receiver(post_save, sender=FoodItem)
def create_drink(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_a_drink:
            DrinkItem.objects.create(
                name=instance.name, thumbnail_image=instance.thumbnail_image
            )


class OrderItem(models.Model):
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_items = models.CharField(max_length=10, default=1)
    drink_quantity = models.IntegerField(default=0)
    drink_metric = models.CharField(max_length=400, default="Ml")
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
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
        ("Order Completed", "Order Completed"),
        ("Order Paid", "Order Paid"),
        ("Order Cancled", "Order Cancled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_note = models.TextField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem)
    status = models.CharField(
        max_length=400, choices=ORDER_STATUS, default="Order Placed"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    cancle_reason = models.TextField(blank=True)

    def ordertotal(self):
        total = 0
        for orderitemm in self.orderitems.all():
            total += orderitemm.totp()
        return total

    def __str__(self):
        return self.user.username + " Ordered " + self.status


class Payment(models.Model):
    PAYMENT_STATUS = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Payment Cancled", "Payment Cancled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ManyToManyField(Order)
    status = models.CharField(max_length=400, choices=PAYMENT_STATUS, default="Unpaid")
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, blank=True
    )
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    cancle_reason = models.TextField(blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def paymenttotal(self):
        total = 0
        for orderitemm in self.order.all():
            for orderitemmm in orderitemm:
                total += orderitemmm.totp()
        return total

    def __str__(self):
        return self.user.username + " Ordered "


class Vat(models.Model):
    vat_name = models.CharField(max_length=400)
    vat_percentage = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.vat_name


class Tax(models.Model):
    tax_name = models.CharField(max_length=400)
    tax_percentage = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.tax_name
