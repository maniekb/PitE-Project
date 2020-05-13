class ChartDataDto:
    def __init__(self, date, high, low, open, close,
                 volume, quoteVolume, weightedAverage):
        self.date = date
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.quoteVolume = quoteVolume
        self.weightedAverage = weightedAverage


def to_chart_data(dct):
    return ChartDataDto(dct['date'], dct['high'], dct['low'], dct['open'],
                           dct['close'], dct['volume'], dct['quoteVolume'], dct['weightedAverage'])
