import calendar

from kryptonite.dataservice.binance_.binance_client import BinanceClient
from kryptonite.dataservice.bitfinex.bitfinex_client import BitfinexClient
from kryptonite.dataservice.bittrex.bittrex_client import BittrexClient
from kryptonite.dataservice.poloniex.client import PoloniexClient


class ChartBuilder:
    def __init__(self, exchange, single_symbol, interval, date_start, date_end):
        self.exchange = exchange
        self.single_symbol = single_symbol
        self.interval = interval
        self.date_start = date_start
        self.date_end = date_end

    def get_to_dollar_data(self):
        if self.exchange == 'binance':
            return self._get_to_dollar_binance_data()
        elif self.exchange == 'poloniex':
            return self._get_to_dollar_poloniex_data()
        elif self.exchange == 'bitfinex':
            return self._get_to_dollar_bitfinex_data()
        elif self.exchange == 'bittrex':
            return self._get_to_dollar_bittrex_data()

    def _get_to_dollar_binance_data(self):
        binance_symbol = self.single_symbol + 'USDT'
        client = BinanceClient()
        data = client.get_historical_data_with_interval(binance_symbol, self.interval, self.date_start, self.date_end)
        li = [{"open_time": record[0], "open": record[1]} for record in data]
        return li

    def _get_to_dollar_poloniex_data(self):
        poloniex_symbol = 'USDT_' + self.single_symbol
        client = PoloniexClient()
        interval = 300
        start = calendar.timegm(self.date_start.utctimetuple())
        end = calendar.timegm(self.date_end.utctimetuple())
        if self.interval == '5m':
            interval = 300
        if self.interval == '1h':
            interval = 1800
        if self.interval in ['1d', '1y']:
            interval = 86400
        data = client.get_chart_data(poloniex_symbol, start, end, interval)
        li = [{"open_time": record.date, "open": record.open} for record in data]
        return li

    def _get_to_dollar_bitfinex_data(self):
        bitfinex_symbol = 't' + self.single_symbol + 'USD'

        client = BitfinexClient()
        interval = self.interval
        start = calendar.timegm(self.date_start.utctimetuple())
        end = calendar.timegm(self.date_end.utctimetuple())
        if interval == '1d':
            interval = '1D'
        data = client.get_historical_data(bitfinex_symbol, start, end, interval)
        li = [{"open_time": record[0], "open": record[1]} for record in data]
        return li

    def _get_to_dollar_bittrex_data(self):
        bittrex_symbol = self.single_symbol + '-USDT'
        interval = self.interval
        client = BittrexClient()
        if interval == '1d':
            interval = 'DAY_1'
        elif interval == '1h':
            interval = 'HOUR_1'
        elif interval == '5m':
            interval = 'MINUTE_5'
        data = client.get_chart_data(bittrex_symbol, self.date_start, self.date_end, interval)
        li = [{"open_time": record["startsAt"], "open": record["open"]} for record in data]
        return li
