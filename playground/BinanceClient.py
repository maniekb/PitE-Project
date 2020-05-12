from Kryptonite.DataService.BinanceClient import BinanceClient
from datetime import  datetime

### Usage
if __name__ == "__main__":
    client = BinanceClient()

    data = client.GetHistoricalDataWithInterval("ICXBTC", "1h", datetime(2020, 5, 1))
    print(data)