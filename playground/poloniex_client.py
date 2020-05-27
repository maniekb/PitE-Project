from kryptonite.dataservice.poloniex.client import PoloniexClient,\
    PoloniexCurrencyPair, PoloniexChartDataCurrencyPair

# example usage PoloniexClinnet.get_currency()
if __name__ == "__main__":
    client = PoloniexClient()
    result = client.get_chart_data(PoloniexChartDataCurrencyPair.USDT_LTC.name,
                                   start='1589035842',
                                   end='1589036502')
    print(len(result))