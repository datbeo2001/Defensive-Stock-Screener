from pathlib import Path
from collections import defaultdict
import datetime as dt
import finnhub as fh
import pandas as pd


def location_input() -> Path:
    while True:
        result_location = Path(input("Please select where you want to save your result: "))
        if result_location.exists() and result_location.is_dir():
            break
        print(f"{result_location} is invalid.")
    return result_location


def name_input() -> str:
    file_name = input("Please give your result a name (don't include the extension): ")
    c_time = dt.datetime.now()
    file_name += f'_{c_time.hour}_{c_time.minute}_{c_time.second}'
    return file_name


def import_or_not() -> bool:
    while True:
        answer = input("Do you want to import your own stock file(yes/no): ")
        if answer.lower() in ('yes', 'no'):
            break
        print("Please type 'yes' or 'no'.")
    return True if answer == 'yes' else False


def list_from_finnhub() -> {str: [str]}:
    exc_file = pd.read_excel("exchange.xlsx")
    exc_list = exc_file.code
    while True:
        exc = input("Please choose your exchange: ")
        exc = exc.upper()
        if exc in exc_list.array:
            break
        print("Invalid exchange. Try again.")
    api_client = fh.Client(api_key='btpvg6v48v6v5kvo1r10')
    raw_data = api_client.stock_symbols(exchange=exc)
    initial_list = defaultdict(list)
    for i in raw_data:
        if i['type'] == "EQS":
            initial_list['ticker'].append(i['symbol'])
    return initial_list


def read_from_excel() -> pd.DataFrame:
    """
    Read from an excel or csv file that contains the
    a list of stocks in the US.
    """
    while True:
        sym_list = Path(input("Please input a file path that contains the list of stocks you want to filter: "))
        if sym_list.exists() and sym_list.is_file() and sym_list.suffix in ('.csv', '.xlsx', '.xlsm'):
            break
        print("Please try again")
    if sym_list.suffix == '.csv':
        data = pd.read_csv(sym_list)
    else:
        data = pd.read_excel(sym_list)
    return data


def create_api_objects(api_key_file) -> [fh.Client]:
    """Get the API keys from the FinnhubAPIkey.txt
    and create a list of CLient objects using those keys.
    There are multiple Client objects since an
    API key can only perform 60 calls/minute."""
    api_objects = []
    for key in api_key_file:
        api_objects.append(fh.Client(api_key=key.rstrip()))
    return api_objects
