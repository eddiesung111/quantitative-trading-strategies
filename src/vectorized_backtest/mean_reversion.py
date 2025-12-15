import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

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

    print(f"--- ADAPTIVE STRATEGY RESULTS ---")
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 8))
    ax1.plot(data.index, data['cumulative_returns'], label = 'Adaptive Strategy', color = 'green')
    ax1.set_title('Cumulative Returns (Dynamic Beta)')
    ax1.grid(True)

    ax2.plot(data.index, data['beta'], label='Rolling Beta (Hedge Ratio)', color='orange')
    ax2.set_title('Rolling Beta (Hedge Ratio)')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
    return

if __name__ == "__main__":
    vectorized_backtest()


