import pytest
import backtrader as bt
import pandas as pd
import datetime as dt
import math
import random
import warnings

# --- SILENCE WARNINGS ---
# Backtrader uses an older datetime method that prints thousands of warnings.
# This silences them for a clean test output.
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- IMPORTS ---
from src.backtest_strategies.strategies.buy_hold import BuyHold
from src.backtest_strategies.strategies.sma_golden_cross import SMAGoldenCross
from src.backtest_strategies.strategies.ema_golden_cross import EMAGoldenCross
from src.backtest_strategies.strategies.macd_strategy import MACDStrategy
from src.backtest_strategies.strategies.rsi_strategy import RSIStrategy
from src.backtest_strategies.strategies.pairs_trading import PairsTrading

# ==========================================
# 🛠️ FIXTURES (Robust Data)
# ==========================================

@pytest.fixture
def mock_trend_data():
    """V-Shape data: Drops then Rockets up. Forces SMA/EMA Crossover."""
    dates = [dt.datetime(2023, 1, 1) + dt.timedelta(days=i) for i in range(300)]
    prices = []
    # Drop 150 -> 100
    for i in range(100):
        prices.append(150 - (i * 0.5))
    # Rocket 100 -> 500
    for i in range(200):
        prices.append(100 + (i * 2))
        
    df = pd.DataFrame({'open': prices, 'high': prices, 'low': prices, 'close': prices, 'volume': 1000}, index=dates)
    return bt.feeds.PandasData(dataname=df, name="TrendStock")

@pytest.fixture
def mock_volatile_data():
    """
    Sine Wave + Non-Zero Noise. 
    Swing from 50 to 150 ensures RSI goes <30 and >70.
    """
    dates = [dt.datetime(2023, 1, 1) + dt.timedelta(days=i) for i in range(200)]
    prices = []
    for i in range(200):
        # Sine wave (amplitude 50) + Random Noise
        base = 100 + 50 * math.sin(i / 10.0) 
        # Ensure noise is never 0.0 to prevent division errors
        noise = random.choice([-2, -1, 1, 2]) * random.random()
        prices.append(base + noise)
        
    df = pd.DataFrame({'open': prices, 'high': prices, 'low': prices, 'close': prices, 'volume': 1000}, index=dates)
    return bt.feeds.PandasData(dataname=df, name="VolatileStock")

@pytest.fixture
def mock_pairs_data():
    """Two correlated stocks with baseline noise."""
    dates = [dt.datetime(2023, 1, 1) + dt.timedelta(days=i) for i in range(200)]
    
    # Stock A: Random walk around 100
    prices_a = [100 + random.uniform(-5, 5) for _ in range(200)]
    
    # Stock B: Follows A, but with noise! 
    # This prevents the spread from being exactly 0.000, establishing a valid StdDev baseline.
    prices_b = [p + random.uniform(-0.5, 0.5) for p in prices_a]
    
    # Create massive divergence (Z-Score spike) in the middle
    for i in range(50, 100):
        prices_b[i] += 10.0 # 10.0 deviation vs 0.5 noise = Huge Z-Score
        
    df_a = pd.DataFrame({'open': prices_a, 'high': prices_a, 'low': prices_a, 'close': prices_a, 'volume': 1000}, index=dates)
    df_b = pd.DataFrame({'open': prices_b, 'high': prices_b, 'low': prices_b, 'close': prices_b, 'volume': 1000}, index=dates)

    return [bt.feeds.PandasData(dataname=df_a, name="StockA"), bt.feeds.PandasData(dataname=df_b, name="StockB")]

# --- HELPER ---
def run_cerebro(strategy_cls, datas, **kwargs):
    cerebro = bt.Cerebro()
    
    # Load Data
    if isinstance(datas, list):
        for d in datas: cerebro.adddata(d)
    else:
        cerebro.adddata(datas)
        
    cerebro.addstrategy(strategy_cls, **kwargs)
    cerebro.broker.set_cash(10000.0)
    
    # FIX: Use FixedSize to guarantee execution
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    
    # FIX: runonce=False avoids ZeroDivision in math indicators
    cerebro.run(runonce=False)
    
    return cerebro.broker.get_value()

# ==========================================
# 🧪 TESTS
# ==========================================

def test_buy_hold(mock_trend_data):
    val = run_cerebro(BuyHold, mock_trend_data)
    assert val > 10000

def test_sma_golden_cross(mock_trend_data):
    val = run_cerebro(SMAGoldenCross, mock_trend_data, fast=20, slow=50)
    assert val > 10000

def test_ema_golden_cross(mock_trend_data):
    val = run_cerebro(EMAGoldenCross, mock_trend_data, fast=20, slow=50)
    assert val > 10000

def test_macd_strategy(mock_volatile_data):
    # Volatile data ensures MACD crosses
    val = run_cerebro(MACDStrategy, mock_volatile_data)
    assert val != 10000

def test_rsi_strategy(mock_volatile_data):
    # Sine wave ensures RSI hits <30 and >70
    val = run_cerebro(RSIStrategy, mock_volatile_data)
    assert val != 10000

def test_pairs_trading(mock_pairs_data):
    val = run_cerebro(PairsTrading, mock_pairs_data)
    assert val != 10000