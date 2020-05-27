from kryptonite.dataservice.binance.binance_client import BinanceClient
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
            return self.get_to_dollar_binance_data()
        elif self.exchange == 'poloniex':
            return self.get_to_dollar_poloniex_data()

    def get_to_dollar_binance_data(self):
        binance_symbol = self.single_symbol + 'USDT'
        client = BinanceClient()
        data = client.get_historical_data_with_interval(binance_symbol, self.interval, self.date_start, self.date_end)
        li = [{"open_time": record[0], "open": record[1]} for record in data]
        return li

    def get_to_dollar_poloniex_data(self):
        poloniex_symbol = 'USDT_' + self.single_symbol
        client = PoloniexClient()
        interval = 300
        start = int(self.date_start.timestamp() + 7200)
        end = int(self.date_end.timestamp() + 7200)
        if self.interval == '5m':
            interval = 300
        if self.interval == '1h':
            interval = 1800
        if self.interval in ['1d', '1y']:
            interval = 86400
        data = client.get_chart_data(poloniex_symbol, start, end, interval)
        li = [{"open_time": record.date, "open": record.open} for record in data]
        return li
