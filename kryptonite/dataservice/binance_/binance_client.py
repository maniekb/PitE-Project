import calendar
from datetime import datetime

from binance.client import Client


class BinanceClient:
    binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
    api_key = 'secret'  # API KEY
    api_secret = 'secret'  # SECRET API KEY
    client = Client(api_key=api_key, api_secret=api_secret)

    # Function returns array of records for specified symbol(e.g 'ICXBTC'), interval('1m', '5m', '1h', '1d')
    # and desired "start day"(datetime(Y,M,D)). Array consists of below arrays
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

    def get_historical_data_with_interval(self, symbol, interval, start, end=None):
        if end is None:
            end = datetime.utcnow()

        klines = self.client.get_historical_klines(symbol, interval, start.strftime("%d %b %Y %H:%M:%S"),
                                                   end.strftime("%d %b %Y %H:%M:%S"))
        return klines

    def get_algorithm_data(self, symbol, interval, start, end):
        milis = self._get_milis_from_interval(interval)
        data = self.get_historical_data_with_interval(symbol, interval, start, end)
        data = self._approximate_missing_intervals(data, start, end, milis)
        return data

    def _approximate_missing_intervals(self, data, start, end, interval_milis):
        start = calendar.timegm(start.utctimetuple()) * 1000
        end = calendar.timegm(end.utctimetuple()) * 1000
        new_data = [dat.copy() for dat in data]
        current = start
        i = 0
        while new_data and current <= end:
            if not i < len(new_data):
                elem = new_data[i - 1].copy()
                elem[0] = current
                new_data.append(elem)
            elif new_data[i][0] != current:
                elem = new_data[i].copy()
                elem[0] = current
                new_data.insert(i, elem)
            current += interval_milis
            i += 1
        return new_data

    def _get_milis_from_interval(self, interval):
        if interval[-1] == 'm':
            return int(interval[:-1]) * 60 * 1000
        elif interval[-1] == 'h':
            return int(interval[:-1]) * 60 * 60 * 1000
        elif interval[-1] == 'd':
            return int(interval[:-1]) * 60 * 60 * 24 * 1000


if __name__ == "__main__":
    a = BinanceClient()
