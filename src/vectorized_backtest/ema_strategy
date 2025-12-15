import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trend_following_strategy():
    ticker = "ADA-USD"
    print(f"Downloading {ticker} data......")

    data = yf.download(ticker, start="2023-01-01", end="2025-01-01")['Close']

    if isinstance(data, pd.Series):
        data = data.to_frame(name='Close')
    else:
        data.columns = ['Close']

    fast_window = 20
    slow_window = 50

    data['fast_ema'] = data['Close'].ewm(span=fast_window, adjust=False).mean()
    data['slow_ema'] = data['Close'].ewm(span=slow_window, adjust=False).mean()

    data['signal'] = 0
    data.loc[data['fast_ema'] > data['slow_ema'], 'signal'] = 1

    data['position'] = data['signal'].shift(1)


    buys = data[data['signal'].diff() == 1]
    sells = data[data['signal'].diff() == -1]


    data['market_return'] = data['Close'].pct_change()
    data['strategy_return'] = data['position'] * data['market_return']
    data['cumulative_return'] = (1 + data['strategy_return']).cumprod()

    total_return = data['cumulative_return'].iloc[-1] - 1
    trades = data["signal"].diff().abs().sum()
    sharpe_ratio = np.sqrt(252) * data['strategy_return'].mean() / data['strategy_return'].std()
    max_drawdown = (data['cumulative_return'] / data['cumulative_return'].cummax() - 1).min()

    print(f"---- Metric Results of {ticker} ----")
    print(f"Strategy Return: {total_return:.2%}")
    print(f"Total Trades:    {int(trades)}")
    print(f"Sharpe Ratio:    {sharpe_ratio:.2f}")
    print(f"Max Drawdown:    {max_drawdown:.2%}")

    # 7. PLOTTING
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

    # Plot Price & EMAs
    ax1.plot(data.index, data['Close'], label="Price", color='black', alpha=0.3)
    ax1.plot(data.index, data['fast_ema'], label='Fast EMA (20)', color="blue", alpha=0.6)
    ax1.plot(data.index, data['slow_ema'], label='Slow EMA (50)', color="orange", alpha=0.6)

    # Plot Scatter Markers
    # Green Up Triangle for Buys
    ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=150, label='Buy Signal', zorder=5)
    # Red Down Triangle for Sells
    ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=150, label='Sell Signal', zorder=5)

    # FIX: Removed int() conversion for ticker
    ax1.set_title(f'Trend Following: Entries & Exits on {ticker}')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True)

    # Plot Returns
    # FIX: Changed 'cum_strategy' to 'cumulative_return'
    ax2.plot(data.index, data['cumulative_return'], label='Trend Strategy', color='green', linewidth=2)
    ax2.set_title(f'Cumulative Returns on {ticker}')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    trend_following_strategy()
