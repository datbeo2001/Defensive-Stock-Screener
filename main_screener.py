from queue import SimpleQueue, Empty
from stock import Stock
import pandas as pd
import time
import finnhub as fh
import logging

criteria = {'PE': ('<', 10), 'PB': ('<=', 0.7), 'CHP': 0.7,
            'RG5Y': ('>=', 10), 'PS': ('<', 1)}
filtered_count = 0
StockQueue = SimpleQueue()
Filtered = SimpleQueue()

logging.basicConfig(format='%(asctime)s  %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


def create_global_queue(sc_list: pd.DataFrame or dict) -> None:
    ticker = None
    if type(sc_list) == pd.DataFrame:
        for i in sc_list.columns:
            if i.lower() in ('ticker', 'symbol'):
                ticker = i
                break
    else:
        ticker = 'ticker'
    logging.info(f"Scanning {len(sc_list[ticker])} stocks.")
    for t in sc_list[ticker]:
        StockQueue.put(t)


def parse_global_queue() -> [Stock]:
    f_list = []

    while True:
        try:
            element = Filtered.get(block=False)
            f_list.append(element)
        except Empty:
            break

    return f_list


def fixed_delay(call, **kwargs) -> dict:
    start = time.perf_counter() + 1
    try:
        ret = call(**kwargs)
    except fh.FinnhubAPIException:
        time.sleep(60)
        ret = call(**kwargs)
    diff = start - time.perf_counter()
    if diff > 0:
        time.sleep(diff)
    return ret


def insert_metrics(data_dict: dict) -> {str: int}:
    """
    Insert the financial metrics from the API calls
    to a dictionary.
    """
    stock_dict = dict()
    try:
        stock_dict['PE'] = data_dict['metric']['peNormalizedAnnual']
        stock_dict['PB'] = data_dict['metric']['pbAnnual']
        stock_dict['RG5Y'] = data_dict['metric']['revenueGrowth5Y']
        stock_dict['PS'] = data_dict['metric']['psTTM']
    except KeyError:
        pass
    return stock_dict


def match_conditions(metrics: {str: int}) -> bool:
    """
    Check if all of the financial metrics satisfy
    the requirements of the criteria.
    """
    count = 0
    for m, v in metrics.items():
        c, t = criteria[m]
        if type(v) in (int, float):
            if c == '>':
                if v > t:
                    count += 1
            elif c == '<':
                if v < t:
                    count += 1
            elif c == '>=':
                if v >= t:
                    count += 1
            elif c == '<=':
                if v <= t:
                    count += 1
    return count == len(criteria) - 1


def filter_undervalued_stocks(api: fh.Client) -> None:
    """Find which column contains the tickers of the file and loop through
    that column of the DataFrame object returned from the read_from_excel
    function and perform API calls on each stock."""
    global filtered_count
    while True:
        try:
            t = StockQueue.get(block=False)
        except Empty:
            break
        data = fixed_delay(api.company_basic_financials, symbol=t, metric='all')
        stock_metrics = insert_metrics(data)
        if stock_metrics != {} and match_conditions(stock_metrics) == True:
            peak_price = data['metric']['52WeekHigh']
            last_price = fixed_delay(api.quote, symbol=t)['l']
            if (last_price / peak_price) <= criteria['CHP']:
                valued_stock = Stock(symbol=t)
                valued_stock.c_price = last_price
                stock_profile = fixed_delay(api.company_profile2, symbol=t)
                if stock_profile != {}:
                    valued_stock.name = stock_profile['name']
                    valued_stock.exchange = stock_profile['exchange']
                    valued_stock.industry = stock_profile['finnhubIndustry']
                    valued_stock.web_url = stock_profile['weburl']
                    valued_stock.market_cap = stock_profile['marketCapitalization'] * 10 ** 6
                Filtered.put(valued_stock)
                filtered_count += 1
                logging.info(f"Filtered {filtered_count} stocks. Symbol is {t}")
