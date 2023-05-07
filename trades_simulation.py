from config import API_KEY
from binance import Binance
import pandas as pd


FUNDING_RATES_FILE_NAME = 'funding_rates.csv'

QUOTE_ASSET_TRADE_BALANCE = 100  # USDT

FIRST_TAKE_PROFIT_RATE = 1.02
SECOND_TAKE_PROFIT_RATE = 1.04
THIRD_TAKE_PROFIT_RATE = 1.06
FOURTH_TAKE_PROFIT_RATE = 1.08
STOP_LOSS_RATE = 0.95


def simulate_trade(prices):
    result = {}
    enter_price = float(prices[0][1])
    asset_balance = QUOTE_ASSET_TRADE_BALANCE / enter_price
    quote_asset_balance = 0
    first_take_profit_reached = False
    first_take_profit_price = enter_price * FIRST_TAKE_PROFIT_RATE
    second_take_profit_reached = False
    second_take_profit_price = enter_price * SECOND_TAKE_PROFIT_RATE
    third_take_profit_reached = False
    third_take_profit_price = enter_price * THIRD_TAKE_PROFIT_RATE
    fourth_take_profit_reached = False
    fourth_take_profit_price = enter_price * FOURTH_TAKE_PROFIT_RATE
    stop_loss_reached = False
    stop_loss_price = enter_price * STOP_LOSS_RATE
    average_sell_price = 0
    times_sell = 0
    for price in prices:
        close_time = price[6]
        high_price = float(price[2])
        low_price = float(price[3])
        if not first_take_profit_reached and first_take_profit_price <= high_price:
            first_take_profit_reached = True
            quote_asset_balance += asset_balance * 0.25 * first_take_profit_price
            asset_balance *= 0.75
            stop_loss_price = enter_price
            average_sell_price = first_take_profit_price
            times_sell += 1
        if not second_take_profit_reached and second_take_profit_price <= high_price:
            second_take_profit_reached = True
            quote_asset_balance += asset_balance * 1/3 * second_take_profit_price
            asset_balance *= 2/3
            average_sell_price = (average_sell_price + second_take_profit_price) / 2
            times_sell += 1
        if not third_take_profit_reached and third_take_profit_price <= high_price:
            third_take_profit_reached = True
            quote_asset_balance += asset_balance * 0.5 * third_take_profit_price
            asset_balance *= 0.5
            average_sell_price = (average_sell_price*2 + third_take_profit_price) / 3
            times_sell += 1
        if not fourth_take_profit_reached and fourth_take_profit_price <= high_price:
            fourth_take_profit_reached = True
            quote_asset_balance += asset_balance * fourth_take_profit_price
            asset_balance = 0
            average_sell_price = (average_sell_price * 3 + fourth_take_profit_price) / 4
            times_sell += 1
            break
        if not stop_loss_reached and stop_loss_price >= low_price:
            stop_loss_reached = True
            quote_asset_balance += asset_balance * stop_loss_price
            asset_balance = 0
            average_sell_price = average_sell_price * (times_sell/4) + stop_loss_price * ((4 - times_sell)/4)
            break
    else:
        last_close_price = float(prices[-1][4])
        quote_asset_balance += asset_balance * last_close_price
        asset_balance = 0
    result['price_buy'] = enter_price
    result['price_sell'] = average_sell_price
    result['profit_loss'] = quote_asset_balance - QUOTE_ASSET_TRADE_BALANCE
    return result


def gather_trades_dataset():
    binance = Binance(API_KEY)
    funding_rates_data = pd.read_csv(FUNDING_RATES_FILE_NAME)
    time_list = []
    symbols_list = []
    buy_prices_list = []
    sell_prices_list = []
    start_fundings_list = []
    profits_losses_list = []
    for index, row in funding_rates_data.iterrows():
        symbol = row['symbols']
        time = row['funding_time']
        prices = binance.get_symbol_prices(symbol, time)
        trade_result = simulate_trade(prices)
        time_list.append(time)
        symbols_list.append(symbol)
        buy_prices_list.append(trade_result['price_buy'])
        sell_prices_list.append(trade_result['price_sell'])
        start_fundings_list.append(row['funding_rate'])
        profits_losses_list.append(trade_result['profit_loss'])
    data = {
        'time': time_list,
        'symbol': symbols_list,
        'price buy': buy_prices_list,
        'price_sell': sell_prices_list,
        'start_funding': start_fundings_list,
        'profit/loss': profits_losses_list
    }
    df = pd.DataFrame(data)
    df.to_csv('trades.csv', index=False)


if __name__ == '__main__':
    gather_trades_dataset()

