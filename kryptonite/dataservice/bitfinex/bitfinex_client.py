import requests


class BitfinexClient:

    # @async_to_sync
    def get_historical_data(self, symbol, start, end, interval):
        start = start * 1000
        end = end * 1000
        milis = self._get_milis_from_interval(interval)
        start, end = self._round_date(start, end, milis)

        url = "https://api-pub.bitfinex.com/v2/candles/trade:{}:{}/hist".format(interval, symbol)
        param = {
            "limit": 10000,
            "start": start,
            "end": end,
            "sort": 1
        }
        response = requests.get(url=url, params=param)
        data = response.json()
        data = self._approximate_missing_intervals(data, start, end, milis)
        return data

        # RESPONSE
        # timestamp (milis)
        # open
        # close
        # high
        # low
        # volume

    def _approximate_missing_intervals(self, data, start, end, interval_milis):
        new_data = [dat.copy() for dat in data]
        current = start
        i = 0
        while new_data and current <= end:
            if not i < len(new_data):
                elem = new_data[i - 1].copy()
                elem[0] = current
                new_data.append(elem)
            elif new_data[i][0] != current:
                elem = new_data[i].copy()
                elem[0] = current
                new_data.insert(i, elem)
            current += interval_milis
            i += 1
        return new_data

    def _get_milis_from_interval(self, interval):
        if interval[-1] == 'm':
            return int(interval[:-1]) * 60 * 1000
        elif interval[-1] == 'h':
            return int(interval[:-1]) * 60 * 60 * 1000
        elif interval[-1] == 'D':
            return int(interval[:-1]) * 60 * 60 * 24 * 1000

    def _round_date(self, start, end, round):
        diff = start % round
        return start - diff, end - diff

# client = BitfinexClient()
# data = client.get_historical_data("tLTCBTC", 1591638060, 1591724700, '5m')
# print(len(data))
# print(data)
# # [print(dat) for dat in data]
