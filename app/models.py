# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
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
    cash_balance = models.IntegerField(default=1000000)

    def __str__(self):
        return f"{self.user} has {self.cash_balance} remaining"

class Papertrading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_amount = models.IntegerField()

    def __str__(self):
        return f"{self.user} bought {self.symbol}"
