import backtrader as bt

class BuyHold(bt.Strategy):
    def __init__(self):
        self.last_day = self.data.datetime.date(-1)
    def next(self):
        if not self.position:
            size = self.broker.get_cash()/ self.data.close[0]
            self.buy(size = size)
        if self.position and self.last_day == self.data.datetime.date(0):
            self.close()
