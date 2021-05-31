# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Watchlist, Cash, Papertrading

# Register your models here.

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol')

class CashAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cash_balance')

class PapertradingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol', 'quantity', 'price', 'total_amount')

admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Cash, CashAdmin)
admin.site.register(Papertrading, PapertradingAdmin)
