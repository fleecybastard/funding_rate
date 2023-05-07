import pandas as pd


def dump_to_excel():
    writer = pd.ExcelWriter('funding.xlsx', engine='xlsxwriter')
    df1 = pd.read_csv('funding_rates.csv', index_col=False)
    df1.to_excel(writer, sheet_name='funding', index=False)
    df2 = pd.read_csv('trades.csv', index_col=False)
    df2.to_excel(writer, sheet_name='trades', index=False)
    df3 = pd.read_csv('trades_analyses.csv', index_col=False)
    df3.to_excel(writer, sheet_name='trades_analyses', index=False)
    writer.close()


if __name__ == '__main__':
    dump_to_excel()