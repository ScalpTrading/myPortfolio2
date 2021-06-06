# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .helpers import *
from datetime import datetime, timezone
import maya
import json
from django.http import JsonResponse

@login_required(login_url="/login/")
def index(request):
    """User dashboard"""

    # Number of articles to load for each symbol in user's watchlist
    article_nos = 2

    # Find logged in user
    user = request.user

    # Logged in user's watchlist symbols
    watchlist_symbols = Watchlist.objects.filter(user=user).values('symbol')
    usr_symbols = []
    for symbol in watchlist_symbols:
        usr_symbols.append(symbol["symbol"])

    # symbol info via IEX cloud batch call
    try:
        symbols = iex_batch_lookup(usr_symbols)
        companyNames = symbols["companyNames"]
        latestPrices = symbols["latestPrices"]
        changePercents = symbols["changePercents"]

        tickers = zip(companyNames, latestPrices, changePercents, usr_symbols)
    except:
        tickers = None

    # Trading view overview gadget symbol input
    try:
        symbol_1 = usr_symbols[0]
    except:
        symbol_1 = None
    try:
        symbol_2 = usr_symbols[1]
    except:
        symbol_2 = None
    try:
        symbol_3 = usr_symbols[2]
    except:
        symbol_3 = None
    try:
        symbol_4 = usr_symbols[3]
    except:
        symbol_4 = None
    try:
        symbol_5 = usr_symbols[4]
    except:
        symbol_5 = None
    try:
        symbol_6 = usr_symbols[5]
    except:
        symbol_6 = None

    # Store articles
    article_sources = []
    article_titles = []
    article_urls = []
    article_publishedAts = []
    article_imgs = []

    if len(usr_symbols) > 0:

        for symbol in usr_symbols:
            # Cap number of articles at 15
            if len(article_sources) > 15:
                break
            # Symbol specific news
            articles = iex_news_lookup(symbol, article_nos)

            for i in range(len(articles)):
                f = articles[i]
                # Only save english language articles
                if f["lang"] == "en":
                    article_sources.append(f["source"])
                    article_titles.append(f["headline"])
                    article_urls.append(f["url"])
                    article_imgs.append(f["image"])

                    # Convert datetime from millisecond epoch to datetime format
                    s = f["datetime"] / 1000
                    dt = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

                    #Parse delta time since article's publishing time
                    dt = maya.parse(dt).datetime().replace(microsecond=0, second=0, minute=0)
                    now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
                    difference = datetime.now(timezone.utc)-maya.parse(dt).datetime()
                    if str(now-dt)[0] == "0":
                        dt_difference = "Less than an hour ago"
                    elif "1 day" in str(now-dt):
                        dt_difference = "over a day ago"
                    elif "2 day" in str(now-dt):
                        dt_difference = "over 2 days ago"
                    else:
                        dt_difference = str(difference.seconds//3600) +" hours ago"
                    article_publishedAts.append(dt_difference)

    symbol_articles = zip(article_sources, article_titles, article_urls, article_publishedAts, article_imgs)

    context = {
        "segment": "index",
        "user": str(user),
        "usr_symbols": usr_symbols,
        "tickers": tickers,
        "symbol_1": symbol_1,
        "symbol_2": symbol_2,
        "symbol_3": symbol_3,
        "symbol_4": symbol_4,
        "symbol_5": symbol_5,
        "symbol_6": symbol_6,
        "symbol_articles": symbol_articles,
    }

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

    # US sports news
    US_sports_articles = news_lookup("US_sports")["articles"]
    US_sports_article_sources = []
    US_sports_article_titles = []
    US_sports_article_urls = []
    US_sports_article_publishedAts = []
    US_sports_article_imgs = []

    for i in range(article_nos):
        f = US_sports_articles[i]
        US_sports_article_sources.append(f["source"]["name"])
        US_sports_article_titles.append(f["title"])
        US_sports_article_urls.append(f["url"])
        US_sports_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        US_sports_article_publishedAts.append(dt_difference)

    US_sports_articles = zip(US_sports_article_sources, US_sports_article_titles, US_sports_article_urls, US_sports_article_publishedAts, US_sports_article_imgs)

    # UK sports news
    UK_sports_articles = news_lookup("UK_sports")["articles"]
    UK_sports_article_sources = []
    UK_sports_article_titles = []
    UK_sports_article_urls = []
    UK_sports_article_publishedAts = []
    UK_sports_article_imgs = []

    for i in range(article_nos):
        f = UK_sports_articles[i]
        UK_sports_article_sources.append(f["source"]["name"])
        UK_sports_article_titles.append(f["title"])
        UK_sports_article_urls.append(f["url"])
        UK_sports_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        UK_sports_article_publishedAts.append(dt_difference)

    UK_sports_articles = zip(UK_sports_article_sources, UK_sports_article_titles, UK_sports_article_urls, UK_sports_article_publishedAts, UK_sports_article_imgs)

    context = {
        "segment": "news",
        "US_gen_articles": US_gen_articles,
        "UK_gen_articles": UK_gen_articles,
        "US_bz_articles": US_bz_articles,
        "UK_bz_articles": UK_bz_articles,
        "US_tech_articles": US_tech_articles,
        "UK_tech_articles": UK_tech_articles,
        "US_sports_articles": US_sports_articles,
        "UK_sports_articles": UK_sports_articles,
    }

    html_template = loader.get_template( 'news.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login")
def finance(request):

    # Number of articles to load
    article_nos = 15

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

    # Financial news
    fin_articles = news_lookup("financial")["articles"]
    fin_article_sources = []
    fin_article_titles = []
    fin_article_urls = []
    fin_article_publishedAts = []
    fin_article_imgs = []

    for i in range(article_nos):
        f = fin_articles[i]
        fin_article_sources.append(f["source"]["name"])
        fin_article_titles.append(f["title"])
        fin_article_urls.append(f["url"])
        fin_article_imgs.append(f["urlToImage"])
        # Parse delta time since article's publishing time
        dt = maya.parse(f["publishedAt"]).datetime().replace(microsecond=0, second=0, minute=0)
        now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
        if str(now-dt)[0] == "0":
            dt_difference = "Less than an hour ago"
        elif str(now-dt)[0] == "1":
            dt_difference = "1 hour ago"
        else:
            dt_difference = str(now-dt)[0]+" hours ago"
        fin_article_publishedAts.append(dt_difference)

    fin_articles = zip(fin_article_sources, fin_article_titles, fin_article_urls, fin_article_publishedAts, fin_article_imgs)

    context = {
        "segment": "finance",
        "US_tickers": US_tickers,
        "US_ETFs_tickers": US_ETFs_tickers,
        "fin_articles": fin_articles,
    }

    html_template = loader.get_template( 'finance.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login")
def quote(request):
    """User symbol quote request"""

    # GET request, user's symbol input
    if request.method == "GET":

        # Obtain user's symbol input
        try:
            symbol = request.GET["symbol"]

        # Stock search page (initial access)
        except:
            context = {
                "segment": "quote"
            }
            html_template = loader.get_template( 'quote-blank.html' )
            return HttpResponse(html_template.render(context, request))

        # If no symbol entered
        if not symbol:
            context = {}

            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))

        # Scrap company stats
        mw_scrapped = mw_lookup(symbol)
        valuation = mw_scrapped["valuation"]
        efficiency = mw_scrapped["efficiency"]
        liquidity = mw_scrapped["liquidity"]
        profitability = mw_scrapped["profitability"]
        capitalization = mw_scrapped["capitalization"]

        if mw_scrapped == None:
            context = {}

            html_template = loader.get_template( 'quote-blank.html' )
            return HttpResponse(html_template.render(context, request))

        # Symbol specific news, initially load 20 articles
        articles = iex_news_lookup(symbol, 20)
        article_sources = []
        article_titles = []
        article_urls = []
        article_publishedAts = []
        article_imgs = []

        if articles == None:
            context = {
                "segment": "quote",
                "error": "We didn't find any symbols matching",
                "symbol": symbol,
            }

            html_template = loader.get_template( 'quote-blank.html' )
            return HttpResponse(html_template.render(context, request))

        for i in range(len(articles)):
            # Load 12 english articles
            if len(article_sources) == 15:
                break
            f = articles[i]
            # Only save english language articles
            if f["lang"] == "en":
                article_sources.append(f["source"])
                article_titles.append(f["headline"])
                article_urls.append(f["url"])
                article_imgs.append(f["image"])

                # Convert datetime from millisecond epoch to datetime format
                s = f["datetime"] / 1000
                dt = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

                #Parse delta time since article's publishing time
                dt = maya.parse(dt).datetime().replace(microsecond=0, second=0, minute=0)
                now = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0)
                difference = datetime.now(timezone.utc)-maya.parse(dt).datetime()
                if str(now-dt)[0] == "0":
                    dt_difference = "Less than an hour ago"
                elif "1 day" in str(now-dt):
                    dt_difference = "over a day ago"
                elif "2 day" in str(now-dt):
                    dt_difference = "over 2 days ago"
                else:
                    dt_difference = str(difference.seconds//3600) +" hours ago"
                article_publishedAts.append(dt_difference)

        symbol_articles = zip(article_sources, article_titles, article_urls, article_publishedAts, article_imgs)

        # Symbol company info
        info = iex_info_lookup(symbol)
        description = info["description"]
        CEO = info["CEO"]
        address = info["address"]
        city = info["city"]
        state = info["state"]
        country = info["country"]
        website = info["website"]
        employees = info["employees"]

        # Check if user has added symbol to watchlist
        user=request.user
        already_exist = Watchlist.objects.filter(user=user, symbol=symbol).exists()

        # Check user's cash balance
        cash_balance = Cash.objects.get(user=user).cash_balance

        # Check user's existing position on symbol
        try:
            quantity = Holdings.objects.get(user=user, symbol=symbol).quantity
        except:
            quantity = 0

        # IEX Cloud API call
        instrument = iex_lookup(symbol)
        # If no data returned
        if not instrument:
            context = {}
            html_template = load.get_template( 'page-403.html' )
            return HttpResponse(html_template.render(context, request))

        else:
            symbol = instrument["symbol"]
            companyName = instrument["companyName"]
            latestPrice = instrument["latestPrice"]
            changePercent = instrument["changePercent"]
            change = instrument["change"]

            context = {
                "segment": "quote",
                "symbol": symbol,
                "companyName": companyName,
                "latestPrice": latestPrice,
                "changePercent": changePercent,
                "change": change,
                "valuation": valuation,
                "efficiency": efficiency,
                "liquidity": liquidity,
                "profitability": profitability,
                "capitalization": capitalization,
                "symbol_articles": symbol_articles,
                "description": description,
                "CEO": CEO,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
                "website": website,
                "employees": employees,
                "already_exist": already_exist,
                # User models
                "cash_balance": cash_balance,
                "quantity": quantity,
            }

            html_template = loader.get_template( 'quote.html' )
            return HttpResponse(html_template.render(context, request))

@csrf_exempt
@login_required(login_url="/login/")
def watchlist(request, symbol):
    """To add/remove symbol to/from user's watchlist"""
    if request.method == "POST":
        # Find logged in user
        user = request.user

        # Check if symbol already exists in User's watchlist
        already_exist = Watchlist.objects.filter(user=user, symbol=symbol).exists()

        # If already exists, remove from watchlist
        if already_exist:
            Watchlist.objects.filter(user=user, symbol=symbol).delete()
            return JsonResponse({
                "user": str(user),
                "message": symbol + " removed from watchlist",
            }, status=201)

        # If doesn't exist, log symbol for user's watchlist
        else:
            newSymbol = Watchlist.objects.create(user=user, symbol=symbol)
            newSymbol.save()
            return JsonResponse({
                "user": str(user),
                "message": symbol + " added to watchlist",
            }, status=201)

@csrf_exempt
@login_required(login_url="/login/")
def buy(request):
    # Get data contents
    data = json.loads(request.body)
    symbol = data.get("symbol", "")
    shares = data.get("shares", "")
    share_price = data.get("share_price", "")
    shares_value = data.get("shares_value", "")

    # Save to papertrading model
    trade = Papertrading(
        user = request.user,
        symbol = symbol,
        quantity = shares,
        price = share_price,
        total_amount = shares_value,
        direction = "Buy",
    )
    trade.save()

    # Update user portfolio holdings
    try:
        # Check user's current holdings for symbol
        user_shares = int(Holdings.objects.get(user=request.user, symbol=symbol).quantity)
        user_avg_price = float(Holdings.objects.get(user=request.user, symbol=symbol).avg_price)
        new_shares = user_shares + int(shares)
        new_avg_price = ( (user_avg_price * user_shares) + float(shares_value) ) / new_shares
        new_total_amount = new_shares * new_avg_price
        # Update number of shares and average share price
        Holdings.objects.filter(user=request.user, symbol=symbol).update(quantity=new_shares)
        Holdings.objects.filter(user=request.user, symbol=symbol).update(avg_price=new_avg_price)
        Holdings.objects.filter(user=request.user, symbol=symbol).update(total_amount=new_total_amount)
    # If user does not hold a position in symbol
    except Holdings.DoesNotExist:
        holding = Holdings(
            user = request.user,
            symbol = symbol,
            quantity = shares,
            avg_price = share_price,
            total_amount = shares_value,
        )
        holding.save()

    # Update user cash balance
    cash_balance = data.get("cash_balance", "")
    new_cash_balance = cash_balance - shares_value
    Cash.objects.filter(user=request.user).update(cash_balance=new_cash_balance)

    return JsonResponse({"message": "Trade complete"}, status=201)

@csrf_exempt
@login_required(login_url="/login/")
def sell(request):
    # Get data contents
    data = json.loads(request.body)
    symbol = data.get("symbol", "")
    shares = data.get("shares", "")
    share_price = data.get("share_price", "")
    shares_value = data.get("shares_value", "")

    # Save to papertrading model
    trade = Papertrading(
        user = request.user,
        symbol = symbol,
        quantity = shares,
        price = share_price,
        total_amount = shares_value,
        direction = "Sell",
    )
    trade.save()

    # Update user portfolio holdings
    try:
        # Check user's current holdings for symbol
        user_shares = int(Holdings.objects.get(user=request.user, symbol=symbol).quantity)
        user_avg_price = float(Holdings.objects.get(user=request.user, symbol=symbol).avg_price)
        new_shares = user_shares - int(shares)
        new_avg_price = user_avg_price
        new_total_amount = new_shares * new_avg_price
        # Update number of shares
        Holdings.objects.filter(user=request.user, symbol=symbol).update(quantity=new_shares)
        # Holdings.objects.filter(user=request.user, symbol=symbol).update(avg_price=new_avg_price)
        Holdings.objects.filter(user=request.user, symbol=symbol).update(total_amount=new_total_amount)
    # If user does not hold a position in symbol
    except Holdings.DoesNotExist:
        return JsonResponse({"error": "User does not hold position in symbol"}, status=401)

    # Update user cash balance
    cash_balance = data.get("cash_balance", "")
    new_cash_balance = cash_balance + shares_value
    Cash.objects.filter(user=request.user).update(cash_balance=new_cash_balance)

    return JsonResponse({"message": "Trade complete"}, status=201)

@login_required(login_url="/login/")
def paper_trading(request):
    """Simulated stock market trading overview page"""

    # Find logged in user
    user = request.user

    # Logged in user's watchlist symbols
    watchlist_symbols = Watchlist.objects.filter(user=user).values('symbol')
    usr_symbols = []
    for symbol in watchlist_symbols:
        usr_symbols.append(symbol["symbol"])

    try:
        companyNames = iex_batch_lookup(usr_symbols)["companyNames"]
        usr_watchlist = zip(usr_symbols, companyNames)
    except:
        usr_watchlist = None

    # Logged in user's holdings
    try:
        symbols = Holdings.objects.filter(user=user).values('symbol')
        holdings_symbols = []
        for symbol in symbols:
            holdings_symbols.append(symbol["symbol"])

        quantities = Holdings.objects.filter(user=user).values('quantity')
        holdings_quantities = []
        for quantity in quantities:
            holdings_quantities.append(quantity["quantity"])

        totals = Holdings.objects.filter(user=user).values('total_amount')
        holdings_totals = []
        for total in totals:
            holdings_totals.append(total["total_amount"])

        # IEX Cloud API call for latest price for holdings symbols
        holdings_latestPrices = []
        for i in range(len(holdings_symbols)):
            instrument = iex_lookup(holdings_symbols[i])
            holdings_latestPrices.append(instrument["latestPrice"])
            holdings_latestPrices[i] = holdings_latestPrices[i]*holdings_quantities[i]

        # Chage in value
        value_changes = []
        for i in range(len(holdings_latestPrices)):
            value_changes.append(round(float(holdings_latestPrices[i]) - float(holdings_totals[i]),2))

        holdings = zip(holdings_symbols, holdings_quantities, holdings_totals, holdings_latestPrices, value_changes)


    # TODO: Get current value of holdings
    # Add additional column for current % weight for each symbol?

    #Other: remove 'cash balance' on paper trading page
    # Other: Holdings page, on click go to quote page for symbol

    except:
        holdings = None

    context = {
        "segment": "paper_trading",
        "usr_watchlist": usr_watchlist,
        "holdings": holdings,

    }

    html_template = loader.get_template( 'paper_trading.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def test(request):
    context = {
        "test": "Dinner?",
    }

    html_template = loader.get_template( 'test.html' )
    return HttpResponse(html_template.render(context, request))
