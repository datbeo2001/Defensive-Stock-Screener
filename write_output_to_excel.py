from collections import defaultdict
from stock import Stock
from pathlib import Path
import pandas as pd
import datetime as dt


def create_file_path(file_name: str, folder_path: Path) -> Path:
    c_time = dt.datetime.now()
    destination = folder_path / f"{file_name}.xlsx"
    return destination


def write_to_excel_and_save(location, u_stocks_data: [Stock]) -> None:
    """Write all of the results on an excel file and place
    the file on the path the users provided."""
    excel_data = defaultdict(list)
    current = dt.datetime.now()
    today = f"{current.month}/{current.day}/{current.year}"
    for stocks in u_stocks_data:
        excel_data['Ticker'].append(stocks.symbol)
        excel_data['Name'].append(stocks.name)
        excel_data['Current Price'].append(stocks.c_price)
        excel_data['Exchange'].append(stocks.exchange)
        excel_data['Industry'].append(stocks.industry)
        excel_data["Company's website"].append(stocks.web_url)
        excel_data["Date"].append(today)
    result_df = pd.DataFrame(excel_data)
    result_df.to_excel(location)
