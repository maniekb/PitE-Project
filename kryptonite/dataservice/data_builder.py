import datetime

# from kryptonite.dataservice.binance.binance_client import BinanceClient
from kryptonite.dataservice.poloniex.client import PoloniexClient, PoloniexChartDataCurrencyPair as PolCurrPair


class AlgorithmData:
    def __init__(self, exchanges=None):
        if exchanges is None:
            exchanges = []
        self.items = exchanges


class Exchange:
    def __init__(self, name, currencies=None, data=None):
        if data is None:
            data = []
        if currencies is None:
            currencies = []
        self.name = name
        self.currencies = currencies
        self.data = data


class ExchangeData:
    def __init__(self, currency, trades=None):
        if trades is None:
            trades = []
        self.currency = currency
        self.trades = trades


class Trade:
    def __init__(self, change_to, records=None):
        if records is None:
            records = []
        self.change_to = change_to
        self.records = records


class Record:
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate


class AlgorithmDataBuilder:
    def __init__(self):
        self.__poloniex_client = PoloniexClient()
        # self.__binance_client = BinanceClient()

    def get_data_last_hour(self):
        end_time = round(datetime.datetime.now().timestamp())  # GMT timezone
        start_time = end_time - 3600
        return self.get_data(start_time, end_time)

    def get_data(self, start, end):
        data = AlgorithmData()
        data.items.append(self.__get_poloniex_data(start, end))
        binance_data = self.__get_binance_data(start, end)
        return data

    def __get_poloniex_data(self, start, end):
        poloniex_data = Exchange("poloniex")
        poloniex_data.currencies.extend(["BTC", "ETH", "ETC"])
        pairs = [PolCurrPair.BTC_ETC, PolCurrPair.BTC_ETH, PolCurrPair.ETH_ETC]
        poloniex_data.data = self.__get_poloniex_currency_data(start, end, poloniex_data.currencies, pairs)
        return poloniex_data

    def __get_poloniex_currency_data(self, start, end, currencies, pairs):
        data = []
        for currency in currencies:
            data.append(ExchangeData(currency))
        for pair in pairs:
            curr = pair.name.split('_')
            records = self.__get_poloniex_pair_data(pair.name, start, end)
            for d in data:
                if d.currency == curr[0]:
                    d.trades.append(Trade(curr[1], records))
                if d.currency == curr[1]:
                    reciprocal = records.copy()
                    for ele in reciprocal:
                        ele.rate = 1.0 / ele.rate
                    d.trades.append(Trade(curr[0], reciprocal))
        return data

    def __get_poloniex_pair_data(self, pair, start, end):
        records = []
        data = self.__poloniex_client.get_chart_data(pair, start, end)
        for ele in data:
            records.append(Record(ele.date, ele.open))
        return records

    def __get_binance_data(self, start, end):
        pass


if __name__ == "__main__":
    data_builder = AlgorithmDataBuilder()
    dat = data_builder.get_data_last_hour()
    for i in dat.items:
        print(i.name)
        for da in i.data:
            print("\t", da.currency)
            for t in da.trades:
                print("\t\t", t.change_to)
