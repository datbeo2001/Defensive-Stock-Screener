from codetiming import Timer
from concurrent.futures import ThreadPoolExecutor
import get_user_input as g_input
import main_screener as screener
import write_output_to_excel as write


def run_program() -> None:
    save_location = g_input.location_input()
    file_name = g_input.name_input()
    answer = g_input.import_or_not()
    if answer:
        stock_list = g_input.read_from_excel()
    else:
        stock_list = g_input.list_from_finnhub()
    t = Timer()
    t.start()
    api_list = g_input.create_api_objects(open("FinnhubAPIkey.txt"))
    screener.create_global_queue(stock_list)
    with ThreadPoolExecutor(max_workers=len(api_list)) as executor:
        executor.map(screener.filter_undervalued_stocks, api_list)
    f_list = screener.parse_global_queue()
    destination = write.create_file_path(file_name, save_location)
    write.write_to_excel_and_save(destination, f_list)
    print(f"Filtering is done. Please check {save_location}.")
    t.stop()


if __name__ == "__main__":
    run_program()
