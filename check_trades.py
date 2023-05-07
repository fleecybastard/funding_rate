import pandas as pd
from trades_simulation import QUOTE_ASSET_TRADE_BALANCE
import matplotlib.pyplot as plt


def gather_trades_analyses():
    trades_df = pd.read_csv('trades.csv')
    amount_of_trades = len(trades_df)
    positive = 0
    negative = 0

    for index, row in trades_df.iterrows():
        if row['profit/loss'] > 0:
            positive += 1
        else:
            negative += 1
    losses = trades_df[trades_df['profit/loss'] <= 0]
    profits = trades_df[trades_df['profit/loss'] > 0]
    max_loss = losses['profit/loss'].min()
    min_loss = losses['profit/loss'].max()
    mean_loss = losses['profit/loss'].mean()
    median_loss = losses['profit/loss'].median()
    max_profit = profits['profit/loss'].max()
    min_profit = profits['profit/loss'].min()
    mean_profit = profits['profit/loss'].mean()
    median_profit = profits['profit/loss'].median()
    plot_pl(trades_df)
    data = {
        'trades': [amount_of_trades],
        'positive_trades': [positive],
        'positive_trades_percentage': [f'{positive / amount_of_trades*100:.2f}%'],
        'negative_trades': [negative],
        'negative_trades_percentage': [f'{negative / amount_of_trades * 100:.2f}%'],
        'min_loss': [min_loss],
        'max_loss': [max_loss],
        'mean_loss': [mean_loss],
        'median_loss': [median_loss],
        'min_profit': [min_profit],
        'max_profit': [max_profit],
        'mean_profit': [mean_profit],
        'median_profit': [median_profit],
    }
    df = pd.DataFrame(data)
    df.to_csv('trades_analyses.csv', index=False)


def plot_pl(trades_df):
    trades_df = trades_df.sort_values(by=['time'])
    initial_budget = QUOTE_ASSET_TRADE_BALANCE * len(trades_df)
    budget = initial_budget
    pnl_list = [0]
    time_list = [float(trades_df.iloc[0]['time']) - 1000]
    for index, trade in trades_df.iterrows():
        budget += trade['profit/loss']
        pnl_list.append(budget - initial_budget)
        time_list.append(trade['time'])
    print(f'INITIAL BALANCE: {initial_budget}')
    print(f'FINAL BALANCE: {budget}')
    plt.plot(time_list, pnl_list)
    plt.show()





if __name__ == '__main__':
    gather_trades_analyses()


