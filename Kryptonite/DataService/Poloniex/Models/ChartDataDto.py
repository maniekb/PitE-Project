class ChartDataDto:
    def __init__(self, date, high, low, open, close,
                 volume, quote_volume, weighted_average):
        self.date = date*1000  #timestamp scaled to miliseconds
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.quote_volume = quote_volume
        self.weighted_average = weighted_average


def to_chart_data(dct):
    return ChartDataDto(dct['date'], dct['high'], dct['low'], dct['open'],
                        dct['close'], dct['volume'], dct['quoteVolume'], dct['weightedAverage'])
