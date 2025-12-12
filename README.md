# Quantitative Trading Strategies Framework

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
├── docs/                               \# Comprehensive documentation files
│   ├── backtrader_setup.md             \# Guide to setting up Backtrader environment
│   └── strategies.md                   \# Detailed descriptions of all trading strategies
├── src/                                \# Source code for strategies and core logic
│   └── backtest_strategies/
│       ├── strategies/                 \# Individual trading strategy implementations
│       └── __init__.py
│       └── __main__.py
│       └── run.py                  
├── tests/                              \# Unit and integration tests for strategies and components
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
cd my-backtest-strategies-v2
```

2.  **Create and activate a virtual environment:**
Before installing any packages or running scripts, you must activate the virtual environment.

* On macOS / Linux:
```bash
source .venv/bin/activate
```

* On Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

* On Windows (Command Prompt):
```DOS
.venv\Scripts\activate.bat
```
You will know the virtual environment is active when your terminal prompt changes to include (.venv) (or similar) at the beginning.

3.  **Install project dependencies:**
```bash
pip install -r requirements.txt
```
This will install `backtrader`, `pandas`, `matplotlib`, and any other required libraries.

## 🧠 Strategies Implemented

This framework includes the following trading strategies:

* **BuyHold:** A baseline strategy that simply buys and holds the asset for the entire backtest period.
* **SMAGoldenCross:** A trend-following strategy based on the crossover of two Simple Moving Averages.
* **EMAGoldenCross:** A trend-following strategy based on the crossover of two Exponential Moving Averages.
* **MACDStrategy:** Utilizes the Moving Average Convergence Divergence indicator for momentum and trend signals.
* **RSIStrategy:** Employs the Relative Strength Index to identify overbought/oversold conditions and potential reversals.

For detailed descriptions, logic, and parameters of each strategy, refer to the [Strategies documentation](https://github.com/eddiesung111/my-backtest-strategies-v2/blob/main/docs/strategies.md).

## Run the program
You can simply use the following command to run the program.
```bash
python3 src/backtest_strategies/run [Strategies]
```
Strategies could be:
* BuyHold
* EMAGoldenCross
* MACDStrategy
* RSIStrategy
* SMAGoldenCross

## ✅ Testing

The project includes a test suite to ensure the correctness and reliability of the strategies and core components.

To run all tests:

```bash
pytest
```

## 📚 Documentation

For more in-depth information, please refer to the `docs/` directory:

* [**Backtrader Setup**](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/docs/backtrader_setup.md): Detailed instructions for setting up your development environment.
* [**Strategies**](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/docs/strategies.md): Comprehensive details on each implemented trading strategy.

## 📄 License

This project is licensed under the [MIT License](https://github.com/eddiesung111/quantitative-trading-strategies/blob/main/LICENSE).
