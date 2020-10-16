class Stock:
    """A class that stores the information of an undervalued stock"""

    def __init__(self, symbol='', name='', c_price=0, exchange='', industry='', weburl='', market_cap=0):
        self.symbol = symbol
        self.name = name
        self.c_price = c_price
        self.exchange = exchange
        self.industry = industry
        self.web_url = weburl
        self.market_cap = market_cap
