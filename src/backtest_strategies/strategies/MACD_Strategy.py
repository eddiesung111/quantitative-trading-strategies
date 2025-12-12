import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (('fast_period', 12),
              ('slow_period', 26),
              ('signal_period', 9),)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        self.macd = bt.indicators.MACD(self.dataclose,
                                       period_me1=self.p.fast_period,       
                                       period_me2=self.p.slow_period,       
                                       period_signal=self.p.signal_period)   

        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()
        else:
            if self.crossover < 0:
                self.order = self.close()

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Rejected]:
            self.order = None