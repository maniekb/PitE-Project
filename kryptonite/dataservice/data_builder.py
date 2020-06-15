from datetime import datetime

from kryptonite.dataservice.binance_.binance_client import BinanceClient
from kryptonite.dataservice.bitfinex.bitfinex_client import BitfinexClient
from kryptonite.dataservice.poloniex.client import PoloniexClient, PoloniexChartDataCurrencyPair as PolCurrPair
from kryptonite.models.models import Exchange as ExchangeModel


class AlgorithmData:
    def __init__(self, exchanges=None):
        if exchanges is None:
            exchanges = []
        self.items = exchanges

    def __dict__(self):
        return {"gielda": [item.__dict__() for item in self.items]}


class Exchange:
    def __init__(self, name, currencies=None, data=None, transaction_fee=None):
        if data is None:
            data = []
        if currencies is None:
            currencies = []
        self.name = name
        self.currencies = currencies
        self.data = data
        self.transaction_fee = transaction_fee

    def __dict__(self):
        return {"nazwa": self.name, "transaction_fee": self.transaction_fee, "currencies": self.currencies,
                "data": [dat.__dict__() for dat in self.data]}


class ExchangeData:
    def __init__(self, currency, trades=None):
        if trades is None:
            trades = []
        self.currency = currency
        self.trades = trades

    def __dict__(self):
        return {"currency": self.currency, "trades": [trade.__dict__() for trade in self.trades]}


class Trade:
    def __init__(self, change_to, records=None):
        if records is None:
            records = []
        self.change_to = change_to
        self.records = records

    def __dict__(self):
        return {"change_to": self.change_to, "records": [record.__dict__() for record in self.records]}


class Record:
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate

    def __dict__(self):
        return {"date": self.date, "rate": self.rate}


class AlgorithmDataBuilder:
    def __init__(self):
        self.__poloniex_client = PoloniexClient()
        self.__binance_client = BinanceClient()
        self.__bitfinex_client = BitfinexClient()

    def get_data_last_hour(self):
        end_time = round(datetime.now().timestamp())  # GMT timezone
        start_time = end_time - 3600 * 3
        return self.get_data(start_time, end_time)

    def get_data(self, start, end):
        data = AlgorithmData()
        start, end = self.__round_date(start, end)
        data.items.append(self.__get_poloniex_data(start, end))
        data.items.append(self.__get_binance_data(start, end))
        data.items.append(self.__get_bitfinex_data(start, end))
        return data

    def __round_date(self, start, end):
        diff = start % 300
        return start - diff, end - diff

    def __get_poloniex_data(self, start, end):
        fee = (ExchangeModel.objects.filter(value='poloniex').first()).transaction_fee
        poloniex_data = Exchange("poloniex", transaction_fee=fee)
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
                    reciprocal = []
                    for rec_index in range(len(records)):
                        reciprocal.append(Record(records[rec_index].date, 1.0 / records[rec_index].rate))
                    d.trades.append(Trade(curr[1], reciprocal))
                if d.currency == curr[1]:
                    d.trades.append(Trade(curr[0], records))
        return data

    def __get_poloniex_pair_data(self, pair, start, end):
        records = []
        data = self.__poloniex_client.get_algo_data(pair, start, end, 300)
        for ele in data:
            if ele.open != 0 and ele.date != 0:
                records.append(Record(ele.date, ele.open))
        return records

    def __get_binance_data(self, start, end):
        fee = (ExchangeModel.objects.filter(value='binance').first()).transaction_fee
        binance_data = Exchange("binance", transaction_fee=fee)
        binance_data.currencies.extend(["BTC", "ETH", "ETC"])
        pairs = [["ETC", "BTC"], ["ETH", "BTC"], ["ETC", "ETH"]]
        binance_data.data = self.__get_binance_currency_data(start, end, binance_data.currencies, pairs)
        return binance_data

    def __get_binance_currency_data(self, start, end, currencies, pairs):
        data = []
        for currency in currencies:
            data.append(ExchangeData(currency))
        for pair in pairs:
            records = self.__get_binance_pair_data(''.join(pair), start, end)
            for d in data:
                if d.currency == pair[0]:
                    d.trades.append(Trade(pair[1], records))
                if d.currency == pair[1]:
                    reciprocal = []
                    for rec_index in range(len(records)):
                        reciprocal.append(Record(records[rec_index].date, 1.0 / records[rec_index].rate))
                    d.trades.append(Trade(pair[0], reciprocal))
        return data

    def __get_binance_pair_data(self, pair, start, end):
        records = []
        start_datetime = datetime.fromtimestamp(start - 7200)
        end_datetime = datetime.fromtimestamp(end - 7200)
        data = self.__binance_client.get_algorithm_data(pair, '5m', start_datetime, end_datetime)
        for ele in data:
            records.append(Record(ele[0], float(ele[1])))
        return records

    def __get_bitfinex_data(self, start, end):
        fee = (ExchangeModel.objects.filter(value='binance').first()).transaction_fee
        bitfinex_data = Exchange("bitfinex", transaction_fee=fee)
        bitfinex_data.currencies.extend(["BTC", "ETH", "ETC", "LTC"])
        pairs = [["ETH", "BTC"], ["ETC", "BTC"], ["LTC", "BTC"]]
        bitfinex_data.data = self.__get_bitfinex_currency_data(start, end, bitfinex_data.currencies, pairs)
        return bitfinex_data

    def __get_bitfinex_currency_data(self, start, end, currencies, pairs):
        data = []
        for currency in currencies:
            data.append(ExchangeData(currency))
        for pair in pairs:
            records = self.__get_bitfinex_pair_data('t' + ''.join(pair), start, end)
            for d in data:
                if d.currency == pair[0]:
                    d.trades.append(Trade(pair[1], records))
                if d.currency == pair[1]:
                    reciprocal = []
                    for rec_index in range(len(records)):
                        reciprocal.append(Record(records[rec_index].date, 1.0 / records[rec_index].rate))
                    d.trades.append(Trade(pair[0], reciprocal))
        return data

    def __get_bitfinex_pair_data(self, pair, start, end):
        records = []
        data = self.__bitfinex_client.get_historical_data(pair, start, end, '5m')
        for ele in data:
            records.append(Record(ele[0], float(ele[1])))
        return records


if __name__ == "__main__":
    data_builder = AlgorithmDataBuilder()
    dat = data_builder.get_data_last_hour()
    for i in dat.items:
        print(i.name)
        for da in i.data:
            print("\t", da.currency)
            for t in da.trades:
                print("\t\t", t.change_to)
                q = 1
                for rec in t.records:
                    print("\t\t\t", q, rec.date, rec.rate)
                    q += 1
