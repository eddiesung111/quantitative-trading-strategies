import backtrader as bt

class SafeDivide(bt.Indicator):
    lines = ('output',)
    params = (('numerator', None), ('denominator', None))

    def __init__(self):
        self.addminperiod(self.params.denominator._minperiod)

    def next(self):
        denom = self.params.denominator[0]
        if denom == 0:
            self.lines.output[0] = 0.0
        else:
            self.lines.output[0] = self.params.numerator[0] / denom

class PairsTrading(bt.Strategy):
    params = (('period', 15), ('devfactor', 2.0), ('qty', 10), ('hedge_ratio', 1.0))

    def __init__(self):
        self.spread = self.datas[0].close - (self.params.hedge_ratio * self.datas[1].close)
        self.spread_mean = bt.indicators.SMA(self.spread, period=self.params.period)
        self.spread_std = bt.indicators.StdDev(self.spread, period=self.params.period)
        numerator = self.spread - self.spread_mean
        self.zscore = SafeDivide(numerator=numerator, denominator=self.spread_std)

    def next(self):
        z = self.zscore[0]
        hedge_qty = int(self.params.qty * self.params.hedge_ratio)

        if not self.position:
            if z > self.params.devfactor:
                self.sell(data=self.datas[0], size=self.params.qty)       
                self.buy(data=self.datas[1], size=hedge_qty)     

            elif z < -self.params.devfactor:
                self.buy(data=self.datas[0], size=self.params.qty)        
                self.sell(data=self.datas[1], size=hedge_qty)
                     
        else:
            if abs(z) < 0.5:
                self.close(data=self.datas[0])
                self.close(data=self.datas[1])
