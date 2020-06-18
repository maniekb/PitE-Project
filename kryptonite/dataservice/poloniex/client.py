import copy
from enum import Enum

from kryptonite.dataservice.poloniex.base import BaseClient
from kryptonite.dataservice.poloniex.models.ChartDataDto import to_chart_data
from kryptonite.dataservice.poloniex.models.TradeHistoryDto import to_trade_history


class PoloniexCurrencyPair(Enum):
    BTC_ETH = 1


class PoloniexChartDataCurrencyPair(Enum):
    USDT_BTC = 1
    USDT_ETH = 2
    USDT_LTC = 3
    BTC_ETH = 4
    BTC_ETC = 5
    BTC_XRP = 6
    BTC_TRX = 7
    BTC_LTC = 8
    ETH_ETC = 9
    TRX_ETH = 10
    TRX_XRP = 11


class PoloniexClient(BaseClient):
    def __init__(self):
        url = "https://poloniex.com/public"
        super().__init__(url)

    def get_currency(self, currency_pair, start, end):
        params = self.__create_params('returnTradeHistory', currency_pair, start, end)
        result = self.get(params)
        trade_history = self.__deserialize_to_trade_history(result)
        return trade_history

    #     period - Valid values are 300, 900, 1800, 7200, 14400, and 86400
    def get_chart_data(self, chart_currency_pair, start, end, period=300):
        params = self.__create_params('returnChartData', chart_currency_pair, start, end, period)
        result = self.get(params)
        data = self.__deserialize_to_chart_data(result)
        return data

    def get_algo_data(self, chart_currency_pair, start, end, period=300):
        data = self.get_chart_data(chart_currency_pair, start, end, period)
        data = self.__approximate_missing_intervals(data, start * 1000, end * 1000, period * 1000)
        return data

    def __create_params(self, command, currency_pair, start, end, period=None):
        params_dict = {'command': command, 'currencyPair': currency_pair, 'start': start, 'end': end, 'period': period}
        return params_dict

    def __deserialize_to_trade_history(self, li):
        result = []
        for item in li:
            result.append(to_trade_history(item))
        return result

    def __deserialize_to_chart_data(self, li):
        result = []
        for item in li:
            result.append(to_chart_data(item))
        return result

    def __approximate_missing_intervals(self, data, start, end, interval_milis):
        new_data = [copy.copy(dat) for dat in data]
        current = start
        i = 0
        while new_data and current <= end:
            if new_data[0].date == 0:
                return []
            if not i < len(new_data):
                elem = copy.copy(new_data[i - 1])
                elem.date = current
                new_data.append(elem)
            elif new_data[i].date != current:
                elem = copy.copy(new_data[i])
                elem.date = current
                new_data.insert(i, elem)
            current += interval_milis
            i += 1
        return new_data
