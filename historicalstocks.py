import urllib2
import json
from bs4 import BeautifulSoup
import re
import pprint as pp

def get_soup(url):
    print url
    try:
        src = urllib2.urlopen(url).read()
    except:
        src = ""
    return BeautifulSoup(src)

def scrape_ticker(ticker_soup):
    data = []
    headers = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    stock_data = ticker_soup.find("table", {"class":"table-data cssTableData"})
    if stock_data is None: return []
    
    for row in stock_data.findAll("tr"):
        row = [cell.text.strip() for cell in row.findAll("td")]
        row = dict(zip(headers, row))
        data.append(row)

    if ticker_soup.find("a", {"id":re.compile("Pager_NextHyperLink")}):
        next_url = ticker_soup.find("a", {"id":re.compile("Pager_NextHyperLink")})['href']
        next_url = "http://www.investopedia.com" + next_url
        next_soup = get_soup(next_url)
        data += scrape_ticker(next_soup)
    
    return [row for row in data if row != []]


url = "http://www.investopedia.com/markets/stocks/{ticker}/historical/?StartDate=8/01/2011&EndDate=9/23/2012&HistoryType=Daily#axzz27KNCmCMb"

tickers = ['goog', 'yhoo', 'emc']

for ticker in tickers:
    soup = get_soup(url.format(ticker=ticker))
    ticker_data = {}
    ticker_data['symbol'] = ticker
    ticker_data['historical'] = scrape_ticker(soup)

    pp.pprint(ticker_data)





