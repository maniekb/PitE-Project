
import json

#pip install pycoingecko https://github.com/man-c/pycoingecko
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

print(json.dumps(cg.get_indexes(),indent=4))

print(cg.get_price(ids='bitcoin,litecoin,ethereum', vs_currencies='BTC'))

#pip install alphavantage https://pypi.org/project/alphavantage/

from alphavantage.price_history import (
  AdjustedPriceHistory, get_results, PriceHistory, IntradayPriceHistory,
  filter_dividends
)

parameters = {'output_size': 'compact', 'period': 'W'}
tickers = ['AAPL', 'MSFT']
results = dict(get_results(PriceHistory, tickers, parameters))
#returns nothing
print(results)