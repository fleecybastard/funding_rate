from config import API_KEY
from binance import Binance
import pandas as pd


def gather_dataset():
    binance = Binance(API_KEY)
    funding_rates = binance.get_funding_rates_in_outlier_zone()
    symbols_list = []
    funding_times_list = []
    funding_rates_list = []
    for funding_rate in funding_rates:
        symbols_list.append(funding_rate['symbol'])
        funding_times_list.append(funding_rate['fundingTime'])
        funding_rates_list.append(float(funding_rate['fundingRate']))
    data = {
        'symbols': symbols_list,
        'funding_time': funding_times_list,
        'funding_rate': funding_rates_list
    }
    df = pd.DataFrame(data)
    df.to_csv('funding_rates.csv', index=False)


if __name__ == '__main__':
    gather_dataset()
