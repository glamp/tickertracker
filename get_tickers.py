import yql
import urllib2, urllib
import json
import pprint as pp
import random
import csv

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
# stocks = ['YHOO', 'APPL', 'GOOG', 'MSFT', 'EMC', 'FB', 'NFLX', '']
stocks = [line.strip() for line in open('tickers.txt').read().split('\n')]
#encapsulate for the query
stocks = ["'" + stock + "'" for stock in stocks]
random.shuffle(stocks)

f = open('companies.txt', 'wb')
w = csv.writer(f)

for i in range(0, len(stocks), 50):
    i_stocks = stocks[i:i+50]
    # define the parameters
    query = {
        "q":"select * from yahoo.finance.stocks where symbol in (%s)" % ', '.join(i_stocks),
        "env":"http://datatables.org/alltables.env",
        "format":"json"
    }

    # create the rest request
    url = base_uri + urllib.urlencode(query)

    rsp = get_json(url)
    quotes = []
    if 'query' in rsp and \
        'results' in rsp['query']\
         and 'stock' in rsp['query']['results']:
        quotes = rsp['query']['results']['stock']

    for quote in quotes:
        w.writerow(quote.values())
        pp.pprint(quote)
        print "*"*80
    print "-"*80

f.close()