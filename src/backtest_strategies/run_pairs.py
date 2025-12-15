import backtrader as bt
import yfinance as yf
from src.backtest_strategies.strategies.pairs_trading import PairsTrading

def run_pairs():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(PairsTrading, hedge_ratio=0.59, qty=100)

    print("Downloading Data for PSX (Phillips 66) and XOM (Exxon)...")

    psx_df = yf.download('PSX', start='2022-01-01', end='2023-01-01', multi_level_index=False).dropna()
    psx_df.columns = [c.lower() for c in psx_df.columns]
    psx_data = bt.feeds.PandasData(dataname=psx_df)

    xom_df = yf.download('XOM', start='2022-01-01', end='2023-01-01', multi_level_index=False).dropna()
    xom_df.columns = [c.lower() for c in xom_df.columns]
    xom_data = bt.feeds.PandasData(dataname=xom_df)

    cerebro.adddata(psx_data, name='PSX')
    cerebro.adddata(xom_data, name='XOM')

    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    cerebro.run()
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='candlestick', volume=False)

if __name__ == '__main__':
    run_pairs()
