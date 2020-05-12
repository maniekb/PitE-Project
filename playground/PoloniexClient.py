from Kryptonite.Clients.Poloniex.client import PoloniexClient,\
    PoloniexCurrencyPair

# example usage PoloniexClinnet.get_currency()
if __name__ == "__main__":
    client = PoloniexClient()
    result = client.get_currency(PoloniexCurrencyPair.BTC_ETH.name,
                                 start='1589035842',
                                 end='1589036502')
    print(len(result))