# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Watchlist

# Register your models here.

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'symbol')

admin.site.register(Watchlist, WatchlistAdmin)
