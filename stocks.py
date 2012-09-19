import urllib2, urllib
import json
import csv
import pprint as pp
import random
import time
from datetime import datetime
import os
import re

def convert_dataypes(x):
    try:
        return float(re.sub('[$-+]', '', x))
    except Exception, e:
        return x

def get_json(url):
    try:
        src = urllib2.urlopen(url).read()
        rsp = json.loads(src)
    except:
        rsp = {}
    return rsp

dirname, filename = os.path.split(os.path.abspath(__file__))

APIKEY = "6YRmn23V34GpcTPULtAmjh.hzXNAh1bcGEL0bl5p6EwUqm25o_FyQZyQrCxisg--"

base_uri = "http://query.yahooapis.com/v1/public/yql?"

# define some stocks
stocks = [line.strip() for line in open(dirname + '/tickers.txt').read().split('\n')]
#encapsulate for the query
stocks = ["'" + stock + "'" for stock in stocks]

random.shuffle(stocks)

f = open('/home/ubuntu/repo/flatfiles/stockdata.csv', 'wb')
w = csv.writer(f)
columns = [u'AfterHoursChangeRealtime', u'AnnualizedGain', u'Ask', u'AskRealtime', u'AverageDailyVolume', u'Bid', u'BidRealtime', u'BookValue', u'Change', u'ChangeFromFiftydayMovingAverage', u'ChangeFromTwoHundreddayMovingAverage', u'ChangeFromYearHigh', u'ChangeFromYearLow', u'ChangePercentRealtime', u'ChangeRealtime', u'Change_PercentChange', u'ChangeinPercent', u'Commission', u'DaysHigh', u'DaysLow', u'DaysRange', u'DaysRangeRealtime', u'DaysValueChange', u'DaysValueChangeRealtime', u'DividendPayDate', u'DividendShare', u'DividendYield', u'EBITDA', u'EPSEstimateCurrentYear', u'EPSEstimateNextQuarter', u'EPSEstimateNextYear', u'EarningsShare', u'ErrorIndicationreturnedforsymbolchangedinvalid', u'ExDividendDate', u'FiftydayMovingAverage', u'HighLimit', u'HoldingsGain', u'HoldingsGainPercent', u'HoldingsGainPercentRealtime', u'HoldingsGainRealtime', u'HoldingsValue', u'HoldingsValueRealtime', u'LastTradeDate', u'LastTradePriceOnly', u'LastTradeRealtimeWithTime', u'LastTradeTime', u'LastTradeWithTime', u'LowLimit', u'MarketCapRealtime', u'MarketCapitalization', u'MoreInfo', u'Name', u'Notes', u'OneyrTargetPrice', u'Open', u'OrderBookRealtime', u'PEGRatio', u'PERatio', u'PERatioRealtime', u'PercebtChangeFromYearHigh', u'PercentChange', u'PercentChangeFromFiftydayMovingAverage', u'PercentChangeFromTwoHundreddayMovingAverage', u'PercentChangeFromYearLow', u'PreviousClose', u'PriceBook', u'PriceEPSEstimateCurrentYear', u'PriceEPSEstimateNextYear', u'PricePaid', u'PriceSales', u'SharesOwned', u'ShortRatio', u'StockExchange', u'Symbol', u'TickerTrend', u'TradeDate', u'TwoHundreddayMovingAverage', u'Volume', u'YearHigh', u'YearLow', u'YearRange', 'datestamp', u'symbol', 'timestamp']
w.writerow(columns)

for block in range(0, len(stocks), 150):
    stocks_subset = stocks[block:block+150]
    # define the parameters
    query = {
        "q":"select * from yahoo.finance.quotes where symbol in (%s)" % ', '.join(stocks_subset),
        "env":"http://datatables.org/alltables.env",
        "format":"json"
    }

    # create the rest request
    url = base_uri + urllib.urlencode(query)

    print url


    rsp = get_json(url)
    quotes = []
    if 'query' in rsp and \
        'results' in rsp['query']\
         and 'quote' in rsp['query']['results']:
        quotes = rsp['query']['results']['quote']

    for quote in quotes:
        for col in quote:
            quote[col] = convert_dataypes(quote[col])

        quote['timestamp'] = int(time.time())
        quote['datestamp'] = str(datetime.now())
        pp.pprint(quote)
        w.writerow([quote.get(col) for col in columns]
        print "*"*80

f.close()









