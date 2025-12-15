import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def don_channel():

    ticker = "RIOT"
    print(f"Downloading {ticker} data...")

    data = yf.download(ticker, start="2022-01-01", end="2024-01-01")['Close']


    if isinstance(data, pd.Series):
        data = data.to_frame(name='Close')
    else:
        data.columns = ['Close']


    entry_window = 20
    exit_window = 10

    data['High_Line'] = data['Close'].rolling(window=entry_window).max().shift(1)
    data['Low_Line'] = data['Close'].rolling(window=exit_window).min().shift(1)


    data['Signal'] = 0
    data.loc[data['Close'] > data['High_Line'], 'Signal'] = 1
    data.loc[data['Close'] < data['Low_Line'], 'Signal'] = -1

    data['Position'] = data['Signal'].replace(0, np.nan).ffill().fillna(0)
    data['Position'] = data['Position'].clip(lower=0)

    buys = data[data['Position'].diff() == 1]
    sells = data[data['Position'].diff() == -1]


    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Position'].shift(1) * data['Return']
    data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()


    total_trades = data['Position'].diff().abs().sum()
    sharpe_ratio = np.sqrt(252) * data['Strategy_Return'].mean() / data['Strategy_Return'].std()

    cum_max = data['Cumulative_Return'].cummax()
    drawdown = (data['Cumulative_Return'] - cum_max) / cum_max
    max_dd = drawdown.min()

    print(f"--- RESULTS: {ticker} ---")
    print(f"Total Trades: {int(total_trades)}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_dd:.2%}")
    print(f"Final Return: {(data['Cumulative_Return'].iloc[-1] - 1):.2%}")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(data.index, data['Close'], label='Price', color='black', alpha=0.5, lw=1)
    ax1.plot(data.index, data['High_Line'], label=f'{entry_window}-Day High', color='green', alpha=0.3, linestyle='--')
    ax1.plot(data.index, data['Low_Line'], label=f'{exit_window}-Day Low', color='red', alpha=0.3, linestyle='--')

    ax1.fill_between(data.index, data['High_Line'], data['Low_Line'], color='gray', alpha=0.1)
    ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=150, label='Buy Breakout', zorder=5)
    ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=150, label='Sell Breakdown', zorder=5)

    ax1.set_title(f'Donchian Channel Breakout: {ticker}')
    ax1.set_yscale('log')
    ax1.legend(loc='upper left')
    ax1.grid(True, which='both', alpha=0.3)


    ax2.plot(data.index, data['Cumulative_Return'], label='Strategy Equity', color='tab:blue', lw=2)
    ax2.plot(data.index, (1 + data['Return']).cumprod(), label='Buy & Hold', color='gray', alpha=0.5, linestyle=':')

    ax2.set_ylabel('Equity')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    don_channel()
