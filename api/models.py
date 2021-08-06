from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


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
    small_note = models.TextField()
    no_of_servings_per_plate = models.CharField(max_length=200)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    CART_STATUS = (("Incart", "Incart"), ("Ordered", "Ordered"))
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items = models.CharField(max_length=10, default=1)
    cart_status = models.CharField(max_length=500, default="Ordered")

    def __str__(self):
        return (
            self.no_of_items + " " + self.food_item.name + " by " + self.user.username
        )

    def totp(self):
        return (self.food_item.price) * (int(self.no_of_items))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_note = models.TextField()
    orderitems = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=400, default="Order Placed")
    orderdate = models.DateTimeField(auto_now_add=True, verbose_name="created")

    def ordertotal(self):
        total = 0
        for orderitemm in self.orderitems.all():
            total += orderitemm.totp()
        return total

    def __str__(self):
        return self.user.username + " Ordered " + self.status
