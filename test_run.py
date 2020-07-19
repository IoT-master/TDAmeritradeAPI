from TDAmeritrade import TDAmeritrade
import ujson
from pprint import pprint


class Usage(TDAmeritrade):
    __slots__ = ['ticker']

    def __init__(self, ticker):
        self.ticker = ticker
        super(Usage, self).__init__()

    async def main(self):
        pprint(await self.get_price_history(self.ticker, 2, 'month', 1, 'weekly', False, startDate='1590987600000', endDate='1594616400000'))


if __name__ == "__main__":
    ticker = 'goog'
    first_instance = Usage(ticker)
