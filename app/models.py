# -*- encoding: utf-8 -*-
"""
Coded by Chris Hui
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} is watching {self.symbol}"

class Cash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=19, decimal_places=2, default=1000000.00)
    # cash_balance = models.IntegerField(default=1000000)

    def __str__(self):
        return f"{self.user} has {self.cash_balance} remaining"

class Holdings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    avg_price = models.DecimalField(max_digits=19, decimal_places=2)
    # avg_price = models.IntegerField()
    # total_amount = models.IntegerField()
    total_amount = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return f"{self.user} has {self.quantity} shares of {self.symbol}"

class Papertrading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    # price = models.IntegerField()
    total_amount = models.DecimalField(max_digits=19, decimal_places=2)
    # total_amount = models.IntegerField()
    direction = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.user} bought {self.symbol}"
