import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib
from datetime import datetime

class MaCrossStrategy(bt.Strategy):

    def __init__(self):
        self.crossovers = []
        for d in self.datas:
            ma_fast = bt.ind.SMA(d, period = 5)
            ma_slow = bt.ind.SMA(d, period=25)

            crossover = bt.ind.CrossOver(ma_fast, ma_slow)
            self.crossovers.append(crossover)


    def next(self):
        for i, d in enumerate(self.datas):
            if not self.getposition(d).size:
                if self.crossovers[i] > 0:
                    self.buy(data=d)
                elif self.crossovers[i] < 0:
                    self.close(data=d)


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # stocks = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'V']
    stocks = ['AAPL', 'MSFT']
    fromdate = datetime(2010,1,1)
    todate = datetime(2021,12,7)
    for s in stocks:

        data = bt.feeds.YahooFinanceData(dataname=s, fromdate=fromdate, todate=todate)
        cerebro.adddata(data, name=s)

    cerebro.addstrategy(MaCrossStrategy)

    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=5.0, commtype=bt.CommInfoBase.COMM_FIXED)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.Transactions, _name='trans')


    back = cerebro.run()

    account_return = cerebro.broker.getvalue()
    print(account_return)

    td = todate -fromdate
    print(account_return/(td.days/365))

