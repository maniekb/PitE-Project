import pandas as pd
from binance.client import Client
from datetime import  datetime


class BinanceClient:
    binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
    api_key = 'secret'    #API KEY
    api_secret = 'secret' #SECRET API KEY
    client = Client(api_key=api_key, api_secret=api_secret)


    #Function returns array of records for specified symbol(e.g 'ICXBTC'), interval('1m', '5m', '1h', '1d')
    #and desired "start day"(datetime(Y,M,D)). Array consists of below arrays
    # [
    #     [
    #         1499040000000,      // Open time
    #         "0.01634790",       // Open
    #         "0.80000000",       // High
    #         "0.01575800",       // Low
    #         "0.01577100",       // Close
    #         "148976.11427815",  // Volume
    #         1499644799999,      // Close time
    #         "2434.19055334",    // Quote asset volume
    #         308,                // Number of trades
    #         "1756.87402397",    // Taker buy base asset volume
    #         "28.46694368",      // Taker buy quote asset volume
    #         "17928899.62484339" // Ignore.
    #     ]
    # ]
    

    def GetHistoricalDataWithInterval(self, symbol, interval, start):
        now = pd.to_datetime(self.client.get_klines(symbol=symbol, interval=interval)[-1][0], unit='ms')

        klines = self.client.get_historical_klines(symbol, interval, start.strftime("%d %b %Y %H:%M:%S"), now.strftime("%d %b %Y %H:%M:%S"))

        return klines

    
