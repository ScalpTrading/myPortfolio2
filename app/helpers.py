from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render

import urllib.parse
import requests
import json
from bs4 import BeautifulSoup

# Helper functions for views.py

def iex_lookup(symbol):
    """iex cloud API: Look up quote for symbol"""
    # IEX Cloud API call documentation: https://intercom.help/iexcloud/en/articles/2851957-how-to-use-the-iex-cloud-api

    # Contact API
    try:
        #api_key = "pk_6d527fd4c0c141e7a54cb4e5e8bb61b0"
        api_key = "pk_55cc84e85d3840ffb346e1f33fcffa7b"
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")

    except:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "symbol": quote["symbol"],
            "companyName": quote["companyName"],
            "latestPrice": float(quote["latestPrice"]),
            "changePercent": round(float(quote["changePercent"])*100,2),
            "change": quote["change"],
        }

    except (KeyError, TypeError, ValueError):
        return None

def iex_batch_lookup(symbols):
    """iex cloud API: Batch look up quote for symbol"""

    tickers_str = ','.join(symbols)

    # Contact API
    try:
        #api_key = "pk_6d527fd4c0c141e7a54cb4e5e8bb61b0"
        api_key = "pk_55cc84e85d3840ffb346e1f33fcffa7b"
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/market/batch?types=quote&symbols={urllib.parse.quote_plus(tickers_str)}&token={api_key}")
        #response = requests.get("https://cloud.iexapis.com/stable/stock/market/batch?types=quote&symbols=QQQ,VOO&token=pk_55cc84e85d3840ffb346e1f33fcffa7b")

    except:
        return None

    # Arrays to store API response
    companyNames = []
    latestPrices = []
    changePercents = []

    # Parse response
    try:
        quotes = response.json()
        for ticker in quotes:
            companyNames.append(quotes[ticker]["quote"]["companyName"])
            latestPrices.append(float(quotes[ticker]["quote"]["latestPrice"]))
            changePercents.append(round(float(quotes[ticker]["quote"]["changePercent"])*100,2))

        return {
            "companyNames": companyNames,
            "latestPrices": latestPrices,
            "changePercents": changePercents,
    }

    except (KeyError, TypeError, ValueError):
        return None

def iex_news_lookup(symbol, no_articles):
    """iex cloud API: News look up for symbol"""

    # Contact API
    try:
        #api_key = "pk_6d527fd4c0c141e7a54cb4e5e8bb61b0"
        api_key = "pk_55cc84e85d3840ffb346e1f33fcffa7b"
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/news/last/{no_articles}?token={api_key}")
        #https://cloud.iexapis.com/stable/stock/AAPL/news?token=pk_6d527fd4c0c141e7a54cb4e5e8bb61b0

    except:
        return None

    try:
        response = response.json()
        return response

    except (KeyError, TypeError, ValueError):
        return None

def iex_info_lookup(symbol):
    """iex cloud API: company about info look up"""

    # Contact API
    try:
        #api_key = "pk_6d527fd4c0c141e7a54cb4e5e8bb61b0"
        api_key = "pk_55cc84e85d3840ffb346e1f33fcffa7b"
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/company?token={api_key}")

    except:
        return None

    try:
        response = response.json()
        return response

    except (KeyError, TypeError, ValueError):
        return None

def av_lookup(symbol):
    """Alpha vantage API lookup"""
    # Alpha Vantage documentation: https://www.alphavantage.co/documentation/

    # Contact API
    try:
        api_key = "OYQK2NGEIKX8AG67"
        overview_response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={urllib.parse.quote_plus(symbol)}&apikey={api_key}")
        quote_response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={urllib.parse.quote_plus(symbol)}&apikey={api_key}")

    except:
        return None

    # Parse response
    try:
        overview = overview_response.json()
        quote = quote_response.json()
        return {
            "companyName": overview["Name"],
            "latestPrice": quote["Global Quote"]["05. price"],
            "changePercent": quote["Global Quote"]["10. change percent"],
        }

    except (KeyError, TypeError, ValueError):
        return None

def news_lookup(region):
    """news API: Look up US top business headlines news articles"""

    # Contact API
    # News API documentation: https://newsapi.org/docs

    # Domains to show on financial news feed, can be modified
    domains = "marketwatch.com,investors.com,barrons.com,proactiveinvestors.co.uk,investing.com,dailyfx.com,bloomberg.com,wsj.com"
    #response = requests.get(f"https://newsapi.org/v2/everything?sortBy=popularity&domains={domains}&apiKey={api_key}")
    try:
        api_key = "67fffc143a5046d48e29f7a3cbbacc88"

        # News by region
        if region == "financial":
            response = requests.get(f"https://newsapi.org/v2/everything?sortBy=publishedAt&domains={domains}&apiKey={api_key}")
        elif region == "US_general":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}")
        elif region == "US_business":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api_key}")
        elif region == "US_technology":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={api_key}")
        elif region == "US_sports":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={api_key}")

        elif region == "UK_general":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=gb&apiKey={api_key}")
        elif region == "UK_business":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=gb&category=business&apiKey={api_key}")
        elif region == "UK_technology":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=gb&category=technology&apiKey={api_key}")
        elif region == "UK_sports":
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=gb&category=sports&apiKey={api_key}")

    except:
        return None

    # Parse repsonse
    try:
        response = response.json()
        return response

    except (KeyError, TypeError, ValueError):
        return None

def mw_lookup(symbol):
    """market watch scrapping"""

    try:
        # Parse website
        response = requests.get(f"https://www.marketwatch.com/investing/stock/{symbol}/company-profile?mod=mw_quote_tab")
        html_soup = BeautifulSoup(response.text, 'html.parser')

        # Extract div containers with class attribute: element element--table
        stats = html_soup.find_all('td', class_ = 'table__cell w75')

    except:
        return None

    # Initialise dicts for scrapped data
    valuation = {}
    efficiency = {}
    liquidity = {}
    profitability = {}
    capitalization = {}

    for stat in stats:
        name = stat.text
        value = stat.next_sibling.next_sibling.text
        category = stat.parent.parent.parent.parent.h2.span.text.lower()
        if category == "valuation":
            valuation[name] = value
        if category == "efficiency":
            efficiency[name] = value
        if category == "liquidity":
            liquidity[name] = value
        if category == "profitability":
            profitability[name] = value
        if category == "capitalization":
            capitalization[name] = value

    return {
        "valuation": valuation,
        "efficiency": efficiency,
        "liquidity": liquidity,
        "profitability": profitability,
        "capitalization": capitalization,
    }
