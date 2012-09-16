import urllib2, urllib
import json
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

f = open('../flatfiles/stockdata.json', 'wb')

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
        f.write(json.dumps(quote) + '\n')
        print "*"*80

f.close()









