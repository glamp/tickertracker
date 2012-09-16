import yql
import urllib2, urllib
import json
import pprint as pp
import random

def get_json(url):
    try:
        src = urllib2.urlopen(url).read()
        rsp = json.loads(src)
    except:
        rsp = {}
    return rsp


APIKEY = "6YRmn23V34GpcTPULtAmjh.hzXNAh1bcGEL0bl5p6EwUqm25o_FyQZyQrCxisg--"

y = yql.Public()

base_uri = "http://query.yahooapis.com/v1/public/yql?"



# define some stocks
stocks = [line.strip() for line in open('tickers.txt').read().split('\n')]
#encapsulate for the query
stocks = ["'" + stock + "'" for stock in stocks]

random.shuffle(stocks)

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
        pp.pprint(quote)
        print "*"*80









