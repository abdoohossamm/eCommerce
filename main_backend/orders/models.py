from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from store.models import Product

User = get_user_model()


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    zipcode = models.PositiveIntegerField(blank=True, null=True)
    place = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)

    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    payment_token = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)
    cash_on_delivery = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name='order_creator', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return f"{self.first_name} at:{self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}"
