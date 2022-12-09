from django.db import models
from api.models import DrinkItem, FoodItem
from django.dispatch import receiver
from django.db.models.signals import post_save


class Feedback(models.Model):
    name = models.CharField(max_length=500, blank=True)
    phone_no = models.CharField(max_length=500, blank=True)
    email = models.CharField(max_length=500, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return self.name
