from fetch_data import fetch_stock_data
from indicators import compute_indicators
from signals import generate_signals
from backtesting import backtest
from gsheet_logger import GSheetLogger
import matplotlib.pyplot as plt


def main():
    tickers = ['RELIANCE.NS','ITC.NS','TCS.NS']
    user_email = input("Enter your email address: ")
    log = GSheetLogger('credentials.json', 'TradingLogSheet', user_email)
    print("Your sheet URL:", log.sheet.url)
    all_results = []
    for ticker in tickers:
        df = fetch_stock_data(ticker, '6mo', '1d')
        df = compute_indicators(df)
        df = generate_signals(df)
        trades, summary = backtest(df, 100000, 0.0)
        print("Summary:", summary)
        print(trades)
        all_results.append((ticker, trades, summary))
        # Visualization
        plt.figure(figsize=(10,4))
        plt.plot(df['Close'], label='Close')
        plt.plot(df['SMA20'], label='SMA20')
        plt.plot(df['SMA50'], label='SMA50')
        plt.scatter(df.loc[df['buy_signal']].index, df.loc[df['buy_signal'],'SMA20'],
                    marker='^', s=100, label='Buy', color='g')
        plt.scatter(df.loc[df['sell_signal']].index, df.loc[df['sell_signal'],'SMA20'],
                    marker='v', s=100, label='Sell', color='r')
        plt.title(ticker)
        plt.legend()
        plt.show()
    log.log_to_sheets(all_results)

if __name__ == "__main__":
    main()