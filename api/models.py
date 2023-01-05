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

    METRICES = (
        ("Ml", "Ml"),
        ("Qtr", "Qtr"),
        ("Half", "Half"),
        ("Full", "Full"),
        ("Glass", "Glass"),
        ("Bootle", "Bottle"),
    )

    DRINK_TYPE = (
        ("Hard Drink", "Hard Drink"),
        ("Soft Drink", "Soft Drink"),
        ("Beer", "Beer"),
        ("Wine", "Wine"),
    )

    category = models.ManyToManyField(FoodCategory)
    name = models.CharField(max_length=500)
    thumbnail_image = models.FileField()
    price = models.IntegerField()
    is_a_drink = models.BooleanField(default=False)
    type_of_drink = models.CharField(
        max_length=100, choices=DRINK_TYPE, default="Soft Drink"
    )
    drink_quantity = models.IntegerField(default=0)
    drink_metric = models.CharField(max_length=400, default="Ml", choices=METRICES)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class DrinkItem(models.Model):

    DRINK_TYPE = (
        ("Hard Drink", "Hard Drink"),
        ("Soft Drink", "Soft Drink"),
        ("Beer", "Beer"),
        ("Wine", "Wine"),
    )

    name = models.CharField(max_length=500)
    thumbnail_image = models.FileField()
    is_a_drink = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    type_of_drink = models.CharField(max_length=100, choices=DRINK_TYPE, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.name


class OrderItem(models.Model):

    ORDER_STATUS = (
        ("Ordered", "Ordered"),
        ("Order Completed", "Order Completed"),
        ("Order Paid", "Order Paid"),
        ("Order Canceled", "Order Canceled"),
        ("Payment Canceled", "Payment Canceled"),
    )

    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_items = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    status = models.CharField(max_length=500, default="Ordered", choices=ORDER_STATUS)

    def __str__(self):
        return (
            str(self.no_of_items)
            + " "
            + self.food_item.name
            + " by "
            + self.user.username
        )

    def totp(self):
        return (self.food_item.price) * (int(self.no_of_items))

    def Total_Price(self):
        return (self.food_item.price) * (int(self.no_of_items))

    def Price_Each(self):
        return self.food_item.price


class Order(models.Model):
    ORDER_STATUS = (
        ("Order Placed", "Order Placed"),
        ("Order Completed", "Order Completed"),
        ("Order Paid", "Order Paid"),
        ("Order Canceled", "Order Canceled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_note = models.TextField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem, related_name="orderitems")
    status = models.CharField(
        max_length=400, choices=ORDER_STATUS, default="Order Placed"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    cancle_reason = models.TextField(blank=True)
    is_kot_printed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def ordertotal(self):
        total = 0
        for orderitemm in self.orderitems.all():
            total += orderitemm.totp()
        return total

    def Order_Total(self):
        total = 0
        for orderitemm in self.orderitems.all():
            total += orderitemm.totp()
        return total

    def Order_Items(self):
        strr = ""
        for orderitemm in self.orderitems.all():
            strr += (
                str(orderitemm.no_of_items)
                + " * "
                + str(orderitemm.Price_Each())
                + "  [ "
                + orderitemm.food_item.name
                + " ] | "
            )
        return strr

    def __str__(self):
        return self.user.username + " Ordered "


class Payment(models.Model):
    PAYMENT_STATUS = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Payment Canceled", "Payment Canceled"),
    )
    DISCOUNT_TYPE = (
        ("Percentage", "Percentage"),
        ("Number", "Number"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ManyToManyField(Order)
    status = models.CharField(max_length=400, choices=PAYMENT_STATUS, default="Unpaid")
    discount_type = models.CharField(
        max_length=400, choices=DISCOUNT_TYPE, default="Number"
    )
    tender_amount = models.FloatField(default=0)
    customer_name = models.CharField(max_length=400, blank=True)
    pan_no = models.CharField(max_length=400, blank=True)
    discount = models.FloatField(default=0)
    discount_percentage = models.IntegerField(default=0)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, blank=True
    )
    payment_remarks = models.TextField(blank=True)
    amount_paidd = models.FloatField(default=0)
    bank_name = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)

    def paymenttotal(self):
        total = 0
        for orderitemm in self.order.all():
            for orderitemmm in orderitemm:
                total += orderitemmm.totp()
        return total

    def __str__(self):
        return self.user.username + " Ordered "


class CanclePayment(models.Model):
    PAYMENT_STATUS = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Payment Canceled", "Payment Canceled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ManyToManyField(Order)
    status = models.CharField(
        max_length=400, choices=PAYMENT_STATUS, default="Payment Canceled"
    )
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
