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

###############################################################################

@login_required(login_url="/login/")
def news(request):

    # Number of articles to load
    article_nos = 10

    # US general news
    US_gen_articles = news_lookup("US_general")["articles"]
    US_gen_article_sources = []
    US_gen_article_titles = []
    US_gen_article_urls = []
    US_gen_article_publishedAts = []
    US_gen_article_imgs = []

    for i in range(article_nos):
        f = US_gen_articles[i]
        US_gen_article_sources.append(f["source"]["name"])
        US_gen_article_titles.append(f["title"])
        US_gen_article_urls.append(f["url"])
        US_gen_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        US_gen_article_publishedAts.append(dt_difference)

    US_gen_articles = zip(US_gen_article_sources, US_gen_article_titles, US_gen_article_urls, US_gen_article_publishedAts, US_gen_article_imgs)

    # UK general news
    UK_gen_articles = news_lookup("UK_general")["articles"]
    UK_gen_article_sources = []
    UK_gen_article_titles = []
    UK_gen_article_urls = []
    UK_gen_article_publishedAts = []
    UK_gen_article_imgs = []

    for i in range(article_nos):
        f = UK_gen_articles[i]
        UK_gen_article_sources.append(f["source"]["name"])
        UK_gen_article_titles.append(f["title"])
        UK_gen_article_urls.append(f["url"])
        UK_gen_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        UK_gen_article_publishedAts.append(dt_difference)

    UK_gen_articles = zip(UK_gen_article_sources, UK_gen_article_titles, UK_gen_article_urls, UK_gen_article_publishedAts, UK_gen_article_imgs)

    # US business news
    US_bz_articles = news_lookup("US_business")["articles"]
    US_bz_article_sources = []
    US_bz_article_titles = []
    US_bz_article_urls = []
    US_bz_article_publishedAts = []
    US_bz_article_imgs = []

    for i in range(article_nos):
        f = US_bz_articles[i]
        US_bz_article_sources.append(f["source"]["name"])
        US_bz_article_titles.append(f["title"])
        US_bz_article_urls.append(f["url"])
        US_bz_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        US_bz_article_publishedAts.append(dt_difference)

    US_bz_articles = zip(US_bz_article_sources, US_bz_article_titles, US_bz_article_urls, US_bz_article_publishedAts, US_bz_article_imgs)

    # UK business news
    UK_bz_articles = news_lookup("UK_business")["articles"]
    UK_bz_article_sources = []
    UK_bz_article_titles = []
    UK_bz_article_urls = []
    UK_bz_article_publishedAts = []
    UK_bz_article_imgs = []

    for i in range(article_nos):
        f = UK_bz_articles[i]
        UK_bz_article_sources.append(f["source"]["name"])
        UK_bz_article_titles.append(f["title"])
        UK_bz_article_urls.append(f["url"])
        UK_bz_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        UK_bz_article_publishedAts.append(dt_difference)

    UK_bz_articles = zip(UK_bz_article_sources, UK_bz_article_titles, UK_bz_article_urls, UK_bz_article_publishedAts, UK_bz_article_imgs)

    # US technology news
    US_tech_articles = news_lookup("US_technology")["articles"]
    US_tech_article_sources = []
    US_tech_article_titles = []
    US_tech_article_urls = []
    US_tech_article_publishedAts = []
    US_tech_article_imgs = []

    for i in range(article_nos):
        f = US_tech_articles[i]
        US_tech_article_sources.append(f["source"]["name"])
        US_tech_article_titles.append(f["title"])
        US_tech_article_urls.append(f["url"])
        US_tech_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        US_tech_article_publishedAts.append(dt_difference)

    US_tech_articles = zip(US_tech_article_sources, US_tech_article_titles, US_tech_article_urls, US_tech_article_publishedAts, US_tech_article_imgs)

    # UK technology news
    UK_tech_articles = news_lookup("UK_technology")["articles"]
    UK_tech_article_sources = []
    UK_tech_article_titles = []
    UK_tech_article_urls = []
    UK_tech_article_publishedAts = []
    UK_tech_article_imgs = []

    for i in range(article_nos):
        f = UK_tech_articles[i]
        UK_tech_article_sources.append(f["source"]["name"])
        UK_tech_article_titles.append(f["title"])
        UK_tech_article_urls.append(f["url"])
        UK_tech_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        UK_tech_article_publishedAts.append(dt_difference)

    UK_tech_articles = zip(UK_tech_article_sources, UK_tech_article_titles, UK_tech_article_urls, UK_tech_article_publishedAts, UK_tech_article_imgs)

    context = {
        "segment": "news",
        "US_gen_articles": US_gen_articles,
        "UK_gen_articles": UK_gen_articles,
        "US_bz_articles": US_bz_articles,
        "UK_bz_articles": UK_bz_articles,
        "US_tech_articles": US_tech_articles,
        "UK_tech_articles": UK_tech_articles,
    }

    html_template = loader.get_template( 'news.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login")
def finance(request):

    # Default stocks, obtain data via IEX Cloud batch request
    default_US_tickers = ["AAPL","MSFT","AMZN","GOOGL","NFLX","BRK.B","TSLA","JPM","V","NVDA","DIS","T","CRM","SE","PINS","ROKU"]
    default_US_ETFs = ["VOO", "VTI", "VXUS", "VEA", "VWO", "QQQ", "QQQJ"]

    # Default US tickers
    try:
        default_US_instruments = iex_batch_lookup(default_US_tickers)
        default_US_companyNames = default_US_instruments["companyNames"]
        default_US_latestPrices = default_US_instruments["latestPrices"]
        default_US_changePercent = default_US_instruments["changePercents"]
        US_tickers = zip(default_US_companyNames, default_US_latestPrices, default_US_changePercent, default_US_tickers)
    except:
        US_tickers = None

    # Default US ETFs
    try:
        default_US_instruments = iex_batch_lookup(default_US_ETFs)
        default_US_ETFs_companyNames = default_US_instruments["companyNames"]
        default_US_ETFs_latestPrices = default_US_instruments["latestPrices"]
        default_US_ETFs_changePercents = default_US_instruments["changePercents"]
        US_ETFs_tickers = zip(default_US_ETFs_companyNames, default_US_ETFs_latestPrices, default_US_ETFs_changePercents, default_US_ETFs)
    except:
        US_ETFs_tickers = None

    context = {
        "segment": "finance",
        "US_tickers": US_tickers,
        "US_ETFs_tickers": US_ETFs_tickers,
    }

    html_template = loader.get_template( 'finance.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def test(request):
    context = {
        "test": "Dinner lol",
    }

    html_template = loader.get_template( 'test.html' )
    return HttpResponse(html_template.render(context, request))
