# -*- encoding: utf-8 -*-
"""
Coded by Chris Hui
"""

from django.contrib import admin
from .models import Watchlist, Cash, Holdings, Papertrading

# Register your models here.

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol')

class CashAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cash_balance')

class HoldingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol', 'quantity', 'avg_price', 'total_amount')

class PapertradingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol', 'quantity', 'price', 'total_amount', 'direction')



admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Cash, CashAdmin)
admin.site.register(Holdings, HoldingsAdmin)
admin.site.register(Papertrading, PapertradingAdmin)
