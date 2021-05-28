# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
     # re_path(r'^.*\.*', views.pages, name='pages'),

    # Added pages
    path("news", views.news, name="news"),
    path("finance", views.finance, name="finance"),
    path("quote_blank", views.quote_blank, name="quote_blank"),
    path("quote", views.quote, name="quote"),
    path("test", views.test, name="test"),


]
