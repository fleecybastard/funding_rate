import requests
from datetime import datetime, timedelta


class Binance:
    def __init__(self, api_key):
        self.__api_key = api_key
        self.__base_url = 'https://www.binance.com/fapi/v1/'
        self.__outlier_zone_value = 0.8 # percent

    def set_outlier_zone_value(self, value):
        if 0 < value < 100:
            self.__outlier_zone_value = value

    def __generate_headers(self):
        return {'X-MBX-APIKEY': self.__api_key}

    def __request(self, url_postfix, params=None):
        if not params:
            params = {}
        url = self.__base_url + url_postfix
        response = requests.get(url, headers=self.__generate_headers(), params=params)
        return response.json()

    def __convert_datetime_to_unix(self, datetime_):
        return str(int(datetime_.timestamp())*1000)

    def __get_symbols(self):
        url_postfix = 'exchangeInfo'
        exchange_info = self.__request(url_postfix)
        exclude_list = ['BTCUSDT_230630', 'ETHUSDT_230630']
        symbols = []
        for symbol_info in exchange_info['symbols']:
            if symbol_info['status'] == 'TRADING' and symbol_info['quoteAsset'] == 'USDT' and \
                    not symbol_info['symbol'] in exclude_list:
                symbols.append(symbol_info['symbol'])
        return symbols

    def get_funding_rates_in_outlier_zone(self):
        symbols = self.__get_symbols()
        funding_rates_in_outlier_zone = []
        for symbol in symbols:
            funding_rate = self.get_funding_rate_in_outlier_zone(symbol, start_time=datetime(year=2022, month=1, day=1), limit=1000)
            if funding_rate:
                funding_rates_in_outlier_zone += funding_rate
        return funding_rates_in_outlier_zone

    def get_funding_rate_in_outlier_zone(self, symbol, start_time=None, end_time=None, limit=None):
        url_postfix = 'fundingRate'
        params = {'symbol': symbol}
        if start_time:
            params['startTime'] = self.__convert_datetime_to_unix(start_time)
        if end_time:
            params['endTime'] = self.__convert_datetime_to_unix(end_time)
        if limit:
            params['limit'] = limit
        funding_rates_in_outlier_zone_for_symbol = []
        funding_rates_info = self.__request(url_postfix, params)
        for funding_rate in funding_rates_info:
            if abs(float(funding_rate['fundingRate'])*100) > self.__outlier_zone_value:
                funding_rates_in_outlier_zone_for_symbol.append(funding_rate)
        return funding_rates_in_outlier_zone_for_symbol

    def get_symbol_prices(self, symbol, start_time: int):
        url_postfix = 'klines'
        params = {'symbol': symbol, 'interval': '1h', 'limit': 1,
                  'startTime': str(start_time),
                  }
        symbol_prices = self.__request(url_postfix, params)
        return symbol_prices

