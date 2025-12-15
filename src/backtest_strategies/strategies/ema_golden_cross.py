import backtrader as bt

class EMAGoldenCross(bt.Strategy):
    params = (('fast', 12), ('slow', 26))

    def __init__(self):
        self.fastMA = bt.indicators.EMA(self.data.close, period=self.params.fast)
        self.slowMA = bt.indicators.EMA(self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fastMA, self.slowMA)

    def next(self):
        if len(self) == self.data.buflen():
            self.close()
            return

        if not self.position:
            if self.crossover > 0:
                # FIX: Use 95% of cash
                cash = self.broker.get_cash() * 0.95
                size = int(cash / self.data.close[0])
                self.buy(size=size)

        elif self.position:
            if self.crossover < 0:
                self.close()
