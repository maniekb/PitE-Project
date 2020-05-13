from Kryptonite.Clients.Poloniex.client import PoloniexClient,\
    PoloniexCurrencyPair, PoloniexCharDataCurrencyPair

# example usage PoloniexClinnet.get_currency()
if __name__ == "__main__":
    client = PoloniexClient()
    result = client.get_chart_data(PoloniexCharDataCurrencyPair.USDT_BTC.name,
                                   start='1589035842',
                                   end='1589036502')
    print(len(result))