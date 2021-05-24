# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from .helpers import *
from datetime import datetime, timezone
import maya

@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def news(request):

    # World news
    articles = news_lookup("US_general")["articles"]
    article_sources = []
    article_titles = []
    article_urls = []
    article_publishedAts = []
    article_imgs = []

    # Load 15 number of articles
    for i in range(15):
        f = articles[i]
        article_sources.append(f["source"]["name"])
        article_titles.append(f["title"])
        article_urls.append(f["url"])
        article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        article_publishedAts.append(dt_difference)

    world_articles = zip(article_sources, article_titles, article_urls, article_publishedAts, article_imgs)

    context = {
        "world_articles": world_articles
    }

    html_template = loader.get_template( 'news.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def test(request):
    context = {
        "test": "Dinner lol",
    }

    html_template = loader.get_template( 'test.html' )
    return HttpResponse(html_template.render(context, request))
