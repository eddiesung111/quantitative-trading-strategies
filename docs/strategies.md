# Trading Strategies Documentation

This document provides a detailed overview of the trading strategies implemented within the project. Each strategy is designed as a `backtrader.Strategy` subclass (or vectorized equivalent), allowing for modular development and easy integration into the backtesting framework.

---

## 1. BuyHold Strategy
The **BuyHold** strategy serves as a fundamental benchmark. It represents a passive investment approach where an asset is purchased at the beginning of the backtest period and held until the end, regardless of market fluctuations.

### Core Logic
* **Entry:** Buys the asset on the first available data point.
* **Exit:** Holds the asset; no active selling is performed. The position is implicitly closed at the end of the backtest.

### Parameters
* *None*

### Assumptions & Considerations
* **Benchmark:** It is crucial for evaluating the performance of active strategies; if an active strategy cannot outperform a simple Buy & Hold, it may not be viable.
* **Costs:** Assumes no transaction costs after the initial buy.
* **Passive:** Does not account for dividends or stock splits beyond what is reflected in the adjusted price data.

---

## 2. SMA Golden Cross Strategy
The **SMA Golden Cross** strategy is a classic trend-following approach that utilizes Simple Moving Averages (SMAs).

### Core Logic
* **Entry (Buy Signal):** Generated when the shorter-period SMA crosses **above** the longer-period SMA (Golden Cross). This indicates a potential bullish trend.
* **Exit (Sell Signal):** Generated when the shorter-period SMA crosses **below** the longer-period SMA (Death Cross). This indicates a potential bearish trend.

### Parameters
* `fast` (int, default: 10): The period for the shorter-term SMA.
* `slow` (int, default: 20): The period for the longer-term SMA.

### Assumptions & Considerations
* **Lag:** SMAs are lagging indicators; they react slower than price.
* **Whipsaws:** Susceptible to false signals in sideways (non-trending) markets.
* **Robustness:** Often used as a foundational system due to its simplicity.

---

## 3. EMA Golden Cross Strategy
Similar to the SMA strategy, but utilizes **Exponential Moving Averages (EMAs)**, which place greater weight on recent price data.

### Core Logic
* **Entry (Buy Signal):** Generated when the shorter-period EMA crosses **above** the longer-period EMA.
* **Exit (Sell Signal):** Generated when the shorter-period EMA crosses **below** the longer-period EMA.

### Parameters
* `fast` (int, default: 5): The period for the shorter-term EMA.
* `slow` (int, default: 20): The period for the longer-term EMA.

### Assumptions & Considerations
* **Reactivity:** Reacts faster to price changes than SMA, potentially catching trends earlier.
* **Noise:** The increased sensitivity can lead to more false signals in choppy markets compared to SMA.

---

## 4. MACD Strategy
The **MACD Strategy** utilizes the Moving Average Convergence Divergence indicator, a momentum oscillator used to reveal the strength, direction, momentum, and duration of a trend.

### Core Logic
* **MACD Line:** Difference between Fast EMA (12) and Slow EMA (26).
* **Signal Line:** 9-period EMA of the MACD Line.
* **Entry (Buy Signal):** Generated when the MACD Line crosses **above** the Signal Line.
* **Exit (Sell Signal):** Generated when the MACD Line crosses **below** the Signal Line.

### Parameters
* `fast_period` (int, default: 12)
* `slow_period` (int, default: 26)
* `signal_period` (int, default: 9)

### Assumptions & Considerations
* **Momentum:** primarily used as a trend-following momentum indicator.
* **Divergence:** Can identify potential reversals when price and MACD diverge.

---

## 5. RSI Strategy
The **RSI Strategy** employs the Relative Strength Index (RSI) to identify overbought or oversold conditions.

### Core Logic
* **Entry (Buy Signal):** Generated when RSI crosses **below** the *oversold* level (e.g., 30) and then crosses back above it.
* **Exit (Sell Signal):** Generated when RSI crosses **above** the *overbought* level (e.g., 70) and then crosses back below it.

### Parameters
* `period` (int, default: 14)
* `oversold_level` (int, default: 30)
* `overbought_level` (int, default: 70)

### Assumptions & Considerations
* **Mean Reversion:** Best used in ranging or consolidating markets.
* **Trend Failure:** Can generate premature exit signals in strong trends (e.g., selling too early in a massive bull run).

---

## 6. Mean Reversion (Bollinger Bands)
The **Mean Reversion** strategy assumes that prices will tend to revert to the average over time. It typically uses Bollinger Bands to define "expensive" and "cheap" zones.

### Core Logic
* **Upper Band:** SMA + (Standard Deviation × `devfactor`).
* **Lower Band:** SMA - (Standard Deviation × `devfactor`).
* **Entry (Buy Signal):** Price closes **below** the Lower Band (asset is oversold).
* **Exit (Sell Signal):** Price closes **above** the Upper Band (asset is overbought) or reverts to the Mean (SMA).

### Parameters
* `period` (int, default: 20): The lookback period for the moving average.
* `devfactor` (float, default: 2.0): The number of standard deviations for the bands.

---

## 7. Donchian Channel Strategy
The **Donchian Channel** strategy is a breakout system commonly used by "Turtle Traders." It relies on breaks of the highest high or lowest low over `n` periods.

### Core Logic
* **Upper Channel:** The highest high of the past `n` periods.
* **Lower Channel:** The lowest low of the past `n` periods.
* **Entry (Buy Signal):** Price breaks **above** the Upper Channel (Trend confirmation).
* **Exit (Sell Signal):** Price breaks **below** the Lower Channel.

### Parameters
* `period` (int, default: 20): The lookback window for highs/lows.

---

## 8. Pairs Trading (Statistical Arbitrage)

The **Pairs Trading** strategy is a market-neutral approach that identifies two cointegrated assets (e.g., GOOG and GOOGL) and trades the spread between them.

### Core Logic
1.  **Cointegration Test:** Check if the spread between Asset A and Asset B is stationary.
2.  **Z-Score Calculation:** Normalize the spread: $Z = \frac{\text{Spread} - \text{Mean}}{\text{StdDev}}$.
3.  **Entry:**
    * **Long the Spread:** If $Z < -\text{threshold}$ (Spread is too low).
    * **Short the Spread:** If $Z > \text{threshold}$ (Spread is too high).
4.  **Exit:** When the Z-Score reverts to zero (Mean Reversion).

### Parameters
* `window` (int, default: 30): Rolling window for Z-score calculation.
* `entry_threshold` (float, default: 2.0): Z-score trigger for entering trades.
* `exit_threshold` (float, default: 0.0): Z-score trigger for closing trades.

### Assumptions & Considerations
* **Market Neutral:** Designed to profit regardless of overall market direction.
* **Breakdown Risk:** The primary risk is that the historical correlation between the two assets breaks down permanently.