from Kryptonite.Clients.base import BaseClient
from Kryptonite.Clients.Poloniex.Models.TradeHistoryDto import to_trade_history
from enum import Enum


class PoloniexCurrencyPair(Enum):
    BTC_ETH = 1


class PoloniexClient(BaseClient):
    def __init__(self):
        url = "https://poloniex.com/public"
        super().__init__(url)

    def get_currency(self, currency_pair, start, end):
        params = self.__create_params('returnTradeHistory', currency_pair, start, end)
        result = self.get(params)
        trade_history = self.__deserialize(result)
        return trade_history

    def __create_params(self, command, currency_pair, start, end):
        params_dict = {}
        params_dict['command'] = command
        params_dict['currencyPair'] = currency_pair
        params_dict['start'] = start
        params_dict['end'] = end
        return params_dict

    def __deserialize(self, li):
        result = []
        for item in li:
            result.append(to_trade_history(item))
        return result
