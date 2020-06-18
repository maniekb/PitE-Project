from datetime import datetime

from bitmex import bitmex


class BitmexClient:
    api_key = '94IFRKCGQj_ViW4KLvCvQ1nO'  # API KEY
    api_secret = 'w9x9w_rYkgc-RPzbEjx1VyItYTUkhOs1pCfAZivRrNqJ-HD9'  # SECRET API KEY
    client = bitmex(test=False, api_key=api_key, api_secret=api_secret)

    # Function returns array of records for specified symbol(e.g 'ICXBTC'), interval('1m', '5m', '1h', '1d')
    # and desired "start day"(datetime(Y,M,D)). Array consists of below arrays
    # [
    #     {
    #         "timestamp": "2020-05-27T13:34:46.996Z",
    #         "symbol": "string",
    #         "open": 0,
    #         "high": 0,
    #         "low": 0,
    #         "close": 0,
    #         "trades": 0,
    #         "volume": 0,
    #         "vwap": 0,
    #         "lastSize": 0,
    #         "turnover": 0,
    #         "homeNotional": 0,
    #         "foreignNotional": 0
    #     }
    # ]

    def get_historical_data_with_interval(self, symbol, interval, start):
        now = datetime.now()
        start = start.strftime("%d %b %Y %H:%M:%S")
        data = \
        self.client.Trade.Trade_getBucketed(symbol=symbol, binSize=interval, startTime=start, endTime=now).result()[0]

        return data
