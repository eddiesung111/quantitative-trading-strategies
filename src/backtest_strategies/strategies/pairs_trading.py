import backtrader as bt

class PairsTrading(bt.Strategy):
    params = (
        ('period', 15),
        ('devfactor', 2.0),
        ('qty', 100),
        ('hedge_ratio', 1.0)
    )

    def __init__(self):
        self.spread = self.datas[0].close - (self.params.hedge_ratio * self.datas[1].close)
        self.spread_mean = bt.indicators.SMA(self.spread, period=self.params.period)
        self.spread_std = bt.indicators.StdDev(self.spread, period=self.params.period)
        self.zscore = (self.spread - self.spread_mean) / self.spread_std

    def next(self):
        hedge_qty = int(self.params.qty * self.params.hedge_ratio)

        if not self.position:
            if self.zscore[0] > self.params.devfactor:
                self.sell(data=self.datas[0], size=self.params.qty)       
                self.buy(data=self.datas[1], size=hedge_qty)              
                print(f"SELL SPREAD: Sold {self.params.qty} PSX, Bought {hedge_qty} XOM | Z: {self.zscore[0]:.2f}")

            elif self.zscore[0] < -self.params.devfactor:
                self.buy(data=self.datas[0], size=self.params.qty)        
                self.sell(data=self.datas[1], size=hedge_qty)             
                print(f"BUY SPREAD: Bought {self.params.qty} PSX, Sold {hedge_qty} XOM | Z: {self.zscore[0]:.2f}")

        else:
            if abs(self.zscore[0]) < 0.5:
                self.close(data=self.datas[0])
                self.close(data=self.datas[1])
                print(f"TAKE PROFIT: Z-Score returned to {self.zscore[0]:.2f}")
