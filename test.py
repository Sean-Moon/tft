import requests
import json
import logging
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
#from .public_api import PublicAPI

import pymongo

class PublicAPI:
    def __init__(self, production=True, version="v1", timeout=20):
        self.__host = production and "https://api.korbit.co.kr/%s/" % version \
                      or "https://api.korbit-test.com/%s/" % version
        self.__timeout = timeout

    # https://apidocs.korbit.co.kr/#public
    def ticker(self, currency_pair="btc_krw"):
        params = {
            'currency_pair': currency_pair
        }
        return self.request_get("ticker", params=params)

    def detailed_ticker(self, currency_pair="btc_krw"):
        params = {
            'currency_pair': currency_pair
        }
        return self.request_get("ticker/detailed", params=params)

    def all_detailed_ticker(self):
        return self.request_get("ticker/detailed/all")

    def orderbook(self, currency_pair="btc_krw", category="all", group=True):
        params = {
            'group': group,
            'category': category,
            'currency_pair': currency_pair
        }
        return self.request_get("orderbook", params=params)

    def bids_orderbook(self, currency_pair="btc_krw", group=True):
        return self.orderbook(currency_pair=currency_pair, category="bid", group=group)

    def asks_orderbook(self, currency_pair="btc_krw", group=True):
        return self.orderbook(currency_pair=currency_pair, category="ask", group=group)

    def list_of_filled_orders(self, currency_pair="btc_krw", interval="hour"):
        params = {
            'time': interval,
            'currency_pair': currency_pair
        }
        return self.request_get("transactions", params=params)

    def request_get(self, path, headers=None, params=None):
        response = requests.get(urljoin(self.host, path), headers=headers, params=params, timeout=self.__timeout)
        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            logging.error("exception: {}, response_text: {}".format(e, response.text))
            return response.text

    def request_post(self, path, headers=None, data=None):
        response = requests.post(urljoin(self.host, path), headers=headers, data=data, timeout=self.__timeout)
        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            logging.error("exception: {}, response_text: {}".format(e, response.text))
            return response.text

    @property
    def host(self):
        return self.__host


print('hello')

__public = PublicAPI()
ticker = __public.ticker
detailed_ticker = __public.detailed_ticker
all_detailed_ticker = __public.all_detailed_ticker
orderbook = __public.orderbook
asks_orderbook = __public.asks_orderbook
bids_orderbook = __public.bids_orderbook
list_of_filled_orders = __public.list_of_filled_orders

print(ticker())
print(detailed_ticker())
#print(all_detailed_ticker())
#print(orderbook())
#print(asks_orderbook())
#print(bids_orderbook())
#print(list_of_filled_orders())
 
conn = pymongo.MongoClient('mongodb://root:root@220.90.208.81:27017/root?authSource=root')
 
#db = conn.root # AAA라는 이름의 데이터베이스 생성
#collection  = db.korbit # test라는 이름의 테이블 생성
db = conn.get_database('root') # 데이터베이스 선택
collection = db.get_collection('korbit') # 테이블 선택
 
## 예시
collection.insert(all_detailed_ticker()) # 선택된 컬렉션에 키가 number, 값이 0인 데이터 저장


import requests
import datetime
#import pandas as pd


def get_ohlc(symbol="BTC", timeunit="day", start=None, end=None, period=None):
    '''
    :param symbol: BTC/ETH/BCH/ETC
    :param timeunit: day/hour/minute
    :param start: 2018-01-01
    :param end: 2018-03-01
    :param period: 5 days
    :return:
    '''
    # HACK
    # - symbol of MED in cryptocompare is MEDIB
    if symbol == "MED":
        symbol = "MEDIB"

    if start == None and end == None:
        end = datetime.datetime.now()
        if period != None:
            assert(period > 0)
            start = end - datetime.timedelta(days=period-1)
        else:
            start = datetime.datetime(2013, 9, 4)
    elif start == None:   # end != None
        end = pd.to_datetime(end)
        if period != None:
            assert(period > 0)
            start = end - datetime.timedelta(days=period-1)
        else:
            start = datetime.datetime(2013, 9, 4)
    elif end == None: # start != None
        start = pd.to_datetime(start)
        if period != None:
            assert(period > 0)
            end = start + datetime.timedelta(days=period-1)
        else:
            end = datetime.datetime.now() #- datetime.timedelta(days=1)
    else:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        if period != None:
            print("period is ignored")

    delta = end - start
    limit = min(2000, delta.days)

    payload = {
        "fsym" : symbol,
        "tsym" : "KRW",
        "e"    : "Korbit",
        "limit": limit,
        "toTs" : int(end.timestamp())
    }

    try:
        url = "https://min-api.cryptocompare.com/data/histo" + timeunit
        r = requests.get(url, params=payload)
        content = r.json()
    except:
        content = None

    if content is not None:
        date_list = [datetime.datetime.fromtimestamp(x['time']) for x in content['Data']]
        df = pd.DataFrame(content['Data'], columns=['open', 'high', 'low', 'close', 'g', 'g', 'f'], index=date_list)
        all_zero_cnt = df.all(axis=1).astype(int).sum()
        if all_zero_cnt > 0:
            print("INFO: all zero " + str(all_zero_cnt) + "row(s) are removed in X-axis")
        return df.loc[df.all(axis=1)]
    else:
        return None


# day
#print(get_ohlc(symbol="BTC", start="2018-02-01", end="2018-02-03"))
#print(get_ohlc(symbol="BTC", period=5))
#print(get_ohlc(symbol="BTC", end="2018-02-03", period=5))

# hour
#print(get_ohlc(symbol="BTC"))
#print(get_ohlc(symbol="BTC", timeunit='hour'))
# /print(get_ohlc(symbol="BTC", timeunit='hour', period=5))

# # minute
#print(get_ohlc(symbol="BTC", timeunit='minute'))
# print(get_ohlc(symbol="BTC", timeunit='minute', period=5))
