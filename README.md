# Quantitative Trading Strategies Framework

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Overview
A modular, event-driven backtesting engine for financial trading strategies. This framework provides clear separation between data handling, strategy logic, execution simulation, and performance analytics.

Designed for quantitative research, allowing for rapid testing of technical signals (SMA, EMA, RSI) and risk metrics.

## 🚀 Features

* **Event-Driven Architecture:** Simulates realistic execution with `DataHandler`, `Strategy`, and `Portfolio` classes.
* **Vectorized Indicators:** Optimized SMA, EMA, MACD, and RSI calculations using Pandas/Numpy.
* **Risk Management:** Built-in calculation of **Value at Risk (VaR)**, Sharpe Ratio, and Maximum Drawdown.
* **Realistic Execution:** Execution handler simulates slippage and commission costs (0.1% default).
* **CI/CD Integration:** GitHub Actions enabled for automated testing.

## 📂 Project Structure
```
.
├── docs/                               # Comprehensive documentation files
│   ├── backtrader_setup.md             # Guide to setting up Backtrader environment
│   └── strategies.md                   # Detailed descriptions of all trading strategies
├── src/                                # Source code for strategies and core logic
│   └── backtest_strategies/
│       ├── strategies/                 # Individual trading strategy implementations
│       │   ├── mean_reversion.py       # Bollinger Band/Z-score strategies
│       │   ├── donchain.py             # Donchian Channel Breakout
│       │   └── ... (SMA, EMA, etc.)
│       ├── pairs_trading.py            # Cointegration-based Pairs Trading logic
│       ├── run_pairs.py                # Runner for Pairs Trading backtests
│       ├── __init__.py
│       ├── __main__.py
│       └── run.py                      # Main runner for single-asset strategies
├── tests/                              # Unit and integration tests
├── .gitignore                       
├── LICENSE
├── README.md          
└── requirements.txt
```

## 🚀 Getting Started

Follow these steps to set up the project and run your first backtest.

### Prerequisites

* **Python:** Recommended versions are **Python 3.10, 3.11, or 3.12**. While Python 3.13 may be used, `backtrader` and its dependencies might exhibit compatibility issues.
* **Git:** For cloning the repository.

### Installation

1.  **Clone the repository:**
```bash
git clone https://github.com/eddiesung111/quantitative-trading-strategies.git
cd quantitative-trading-strategies
```

2.  **Create and activate a virtual environment:**
Before installing any packages or running scripts, you must activate the virtual environment.

* On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

* On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

You will know the virtual environment is active when your terminal prompt changes to include (.venv) (or similar) at the beginning.

3.  **Install project dependencies:**
```bash
pip install -r requirements.txt
```

## 🧠 Strategies Implemented
This framework includes the following trading strategies. For detailed logic and parameters, refer to [docs/strategies.md](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/docs/strategies.md).

### Single-Asset Strategies
| Strategy | Description |
| :--- | :--- |
| **BuyHold** | A baseline strategy that simply buys and holds the asset for the entire period. |
| **SMAGoldenCross** | Trend-following strategy based on the crossover of two Simple Moving Averages. |
| **EMAGoldenCross** | Trend-following strategy based on the crossover of two Exponential Moving Averages. |
| **MACDStrategy** | Utilizes Moving Average Convergence Divergence for momentum and trend signals. |
| **RSIStrategy** | Employs Relative Strength Index to identify overbought/oversold conditions. |
| **MeanReversion** | Captures price reversions to the mean (e.g., Bollinger Bands). |
| **Donchain** | Breakout strategy using Donchian Channels to capture volatility expansion. |

### Multi-Asset Strategies
| Strategy | Description |
| :--- | :--- |
| **PairsTrading** | Statistical Arbitrage strategy identifying cointegrated pairs to trade the spread. |

## 🏃 Run the Program
1. To execute a standard technical analysis strategy:
```bash
python3 src/backtest_strategies/run.py [StrategyName]
```
Available Strategies:
* `BuyHold`
* `EMAGoldenCross`
* `MACDStrategy`
* `RSIStrategy`
* `SMAGoldenCross`
* `MeanReversion`
* `Donchain`
Example
```bash
python3 src/backtest_strategies/run.py Donchain
```
2. Run Pairs Trading (Statistical Arbitrage)
To execute the cointegration-based pairs trading engine:
```bash
python3 src/backtest_strategies/run_pairs.py
```

## ✅ Testing
The project includes a test suite to ensure the correctness and reliability of the strategies and core components.
To run all tests:
```bash
pytest
```

## 📚 Documentation
For more in-depth information, please refer to the docs/ directory:
* [**Backtrader Setup**](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/docs/backtrader_setup.md): Detailed instructions for setting up your development environment.
* [**Strategies**](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/docs/strategies.md): Comprehensive details on each implemented trading strategy.
