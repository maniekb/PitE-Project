import calendar
from datetime import datetime

import requests


class BittrexClient:

    def get_chart_data(self, symbol, start, end, interval):
        url = "https://api.bittrex.com/v3/markets/{}/candles/{}/recent".format(symbol, interval)
        response = requests.get(url=url)
        data = response.json()
        data = self._swap_datetime_with_mili_timestamp(data)
        data = [record for record in data if
                datetime.fromtimestamp(record["startsAt"] / 1000) >= start]

        return data

    def get_algorithm_data(self, symbol, start, end, interval):
        end_date = datetime.utcfromtimestamp(end).date()
        start_date = datetime.utcfromtimestamp(start).date()
        if end_date == start_date:
            if end_date == datetime.utcnow().date():
                url = "https://api.bittrex.com/v3/markets/{}/candles/{}/recent".format(symbol, interval)
                response = requests.get(url=url)
                data = response.json()
                data = self._swap_datetime_with_mili_timestamp(data)
                data = [record for record in data if start * 1000 <= record["startsAt"] <= end * 1000]
            else:
                url = "https://api.bittrex.com/v3/markets/{symbol}/candles/{interval}/historical/{year}/{month}/{day}".format(
                    symbol=symbol, interval=interval, year=end_date.year, month=end_date.month, day=end_date.day)
                response = requests.get(url=url)
                data = response.json()
                data = self._swap_datetime_with_mili_timestamp(data)
                data = [record for record in data if start * 1000 <= record["startsAt"] <= end * 1000]
        else:
            data = []
            if end_date == datetime.utcnow().date():
                url = "https://api.bittrex.com/v3/markets/{}/candles/{}/recent".format(symbol, interval)
                response = requests.get(url=url)
                data = response.json()
                data = self._swap_datetime_with_mili_timestamp(data)
                data = [record for record in data if start * 1000 <= record["startsAt"] <= end * 1000]
            else:
                for date in [end_date, start_date]:
                    url = "https://api.bittrex.com/v3/markets/{symbol}/candles/{interval}/historical/{year}/{month}/{day}".format(
                        symbol=symbol, interval=interval, year=date.year, month=date.month, day=date.day)
                    response = requests.get(url=url)
                    temp_data = response.json()
                    temp_data = self._swap_datetime_with_mili_timestamp(temp_data)
                    temp_data = [record for record in temp_data if start * 1000 <= record["startsAt"] <= end * 1000]
                    data.extend(temp_data)
        return data

    def _swap_datetime_with_mili_timestamp(self, data):
        for record in data:
            record["startsAt"] = int(
                calendar.timegm(datetime.strptime(record["startsAt"], "%Y-%m-%dT%H:%M:%SZ").utctimetuple())) * 1000
        return data
