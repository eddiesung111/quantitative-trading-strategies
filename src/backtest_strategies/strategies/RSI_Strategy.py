import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_Safe(self.data.close, period=self.params.rsi_period)

    def next(self):
        if not self.position:
            if self.rsi[0] < self.params.rsi_oversold:
                size = int((self.broker.get_cash() * 0.95) / self.data.close[0])
                if size > 0:
                    self.buy(size=size)
        else:
            if self.rsi[0] > self.params.rsi_overbought:
                self.close()
