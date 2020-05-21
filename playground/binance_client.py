from kryptonite.dataservice.binance.binance_client import BinanceClient
from datetime import  datetime

### Usage
if __name__ == "__main__":
    client = BinanceClient()

    data = client.get_historical_data_with_interval("ICXBTC", "1h", datetime(2020, 5, 1))
    print(data)