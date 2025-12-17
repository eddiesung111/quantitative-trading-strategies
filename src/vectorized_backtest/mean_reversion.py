import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

def vectorized_backtest():
    tickers = ['XOM', 'CVX']
    data = yf.download(tickers, start='2023-01-01', end='2025-01-01')['Close']
    data = data.dropna()

    # Calculate rolling OLS
    window = 70
    y = data['CVX']
    X = sm.add_constant(data['XOM'])

    model = RollingOLS(y, X, window = window)
    rolling_res = model.fit()

    data['beta'] = rolling_res.params['XOM']
    data = data.dropna()

    data['spread'] = data['CVX'] - (data['beta'] * data['XOM'])

    z_window = 35
    data['mean'] = data['spread'].rolling(window = z_window).mean()
    data['std'] = data['spread'].rolling(window = z_window).std()
    data['z_score'] = (data['spread'] - data['mean']) / data['std']

    data['signal'] = 0
    entry_thresold = 2.0

    data.loc[data['z_score'] > entry_thresold, 'signal'] = -1
    data.loc[data['z_score'] < -entry_thresold, 'signal'] = 1

    data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
    data.loc[abs(data['z_score']) < 0.5, 'position'] = 0

    returns_cvx = data['CVX'].pct_change()
    returns_xom = data['XOM'].pct_change()

    data['strategy_returns'] = data['position'].shift(1) * (returns_cvx - returns_xom * data['beta'].shift(1))
    data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()

    total_return = data['cumulative_returns'][-1] - 1
    sharpe_ratio = data['strategy_returns'].mean() / data['strategy_returns'].std() * np.sqrt(252)
    trades = data['signal'].diff().abs().sum()
    max_drawdown = (data['cumulative_returns'] / data['cumulative_returns'].cummax() - 1).min()

    print(f"--- ADAPTIVE STRATEGY RESULTS ---")
    print(f"Total Trades:    {int(trades)}")
    print(f"Sharpe Ratio:    {sharpe_ratio:.2f}")
    print(f"Max Drawdown:    {max_drawdown:.2%}")
    print(f"Strategy Return: {total_return:.2%}")


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(data.index, data['cumulative_returns'], label = 'Adaptive Strategy', color = 'blue', lw = 1.5, alpha = 0.7)
    ax1.set_title('Cumulative Returns (Dynamic Beta)')
    ax1.grid(True)

    ax2.plot(data.index, data['beta'], label='Rolling Beta (Hedge Ratio)', color='orange', lw = 1, alpha = 0.7)
    ax2.set_title('Rolling Beta (Hedge Ratio)')
    ax2.grid(True)

    plt.tight_layout()
    file_name = "results/mean_reversion_strategy.png"
    plt.savefig(file_name)
    print(f"Figure saved as {file_name}")
    plt.show()

if __name__ == "__main__":
    vectorized_backtest()


