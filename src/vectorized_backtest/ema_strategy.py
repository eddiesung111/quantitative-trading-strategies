import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ema_strategy():
    ticker = "ETH-USD"
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
    print(f"Total Trades:    {int(trades)}")
    print(f"Sharpe Ratio:    {sharpe_ratio:.2f}")
    print(f"Max Drawdown:    {max_drawdown:.2%}")
    print(f"Strategy Return: {total_return:.2%}")
    

    # 7. PLOTTING
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})

    # Plot Price & EMAs
    ax1.plot(data.index, data['Close'], label="Price", color='black', alpha=0.5, lw = 1)
    ax1.plot(data.index, data['fast_ema'], label='Fast EMA (20)', color="blue", alpha=0.3, linestyle='--')
    ax1.plot(data.index, data['slow_ema'], label='Slow EMA (50)', color="orange", alpha=0.3, linestyle='--')

    # Plot Scatter Markers
    ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=150, label='Buy Signal', zorder=5)
    ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=150, label='Sell Signal', zorder=5)

    ax1.set_title(f'SMA Strategy: Entries & Exits on {ticker}')
    ax1.set_yscale('log')
    ax1.legend(loc='upper left')
    ax1.grid(True, which='both', alpha=0.3)

    # Plot Returns
    ax2.plot(data.index, data['cumulative_return'], label='Trend Strategy', color='blue', lw=2)
    ax2.plot(data.index, (1 + data['market_return']).cumprod(), label='Buy & Hold', color='gray', alpha=0.5, linestyle=':')
    ax2.set_title(f'Cumulative Returns on {ticker}')

    ax2.set_ylabel('Equity')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    file_name = "results/ema_strategy.png"
    plt.savefig(file_name)
    print(f"Figure saved as {file_name}")
    plt.show()

if __name__ == "__main__":
    ema_strategy()