import analysis.BullishDetector
from multiprocessing import Pool
import numpy as np
import time
import retriever.StockDataRetriever as retriever
import analysis.LevelDetector as levels


def closest(lst, k):
    lst = np.asarray(lst)
    idx = (np.abs(lst - k)).argmin()
    return lst[idx]


def analyze_stock(symbol, start_date, end_date):
    result = ""
    data = retriever.StockDataRetriever(symbol, start_date, end_date)
    if analysis.BullishDetector.BullishDetector.is_hammer(data):
        result += ", hammer"
    if analysis.BullishDetector.BullishDetector.is_inverted_hammer(data):
        result += ", inverted hammer"
    if analysis.BullishDetector.BullishDetector.is_bullish_engulfing(data):
        result += ", bullish engulfing"
    if analysis.BullishDetector.BullishDetector.is_morning_star(data):
        result += ", morning star"
    if analysis.BullishDetector.BullishDetector.is_piercing_line(data):
        result += ", piercing line"
    if analysis.BullishDetector.BullishDetector.is_three_white_soldiers(data):
        result += ", three white soldiers"

    if not result:
        return None
    else:
        low_today = data.getLow(0)
        support_detector = levels.LevelDetector(data)
        support_level_prices = support_detector.get_support_level_prices()
        closest_support_price = closest(support_level_prices, low_today)
        percent_difference = low_today/closest_support_price
        if 1.00 < percent_difference < 1.05:
            result += ", support"

            # Replace the first instance of a comma in the Result list
            result = result.replace(", ", "", 1)
            return symbol, result


def get_stock_symbols(file_name):
    file = open(file_name, "r")
    return str(file.read()).splitlines()


def run_multiprocessing(stock_symbols, start_date, end_date):
    start = time.time()

    values = []
    buy_stocks = []
    for symbol in stock_symbols:
        values.append((symbol, start_date, end_date))

    with Pool() as pool:
        res = pool.starmap(analyze_stock, values)

    for symbol in res:
        if symbol is not None:
            buy_stocks.append(symbol[0])

    end = time.time()
    print("time to run: " + str(end - start))
    return buy_stocks


if __name__ == '__main__':
    stock_symbols = get_stock_symbols("test_stocks.txt")
    start_date = "2020-01-01"
    end_date = "2021-08-03"
    buy_date = "2021-08-03"
    today = "2021-08-31"
    buy_stocks = run_multiprocessing(stock_symbols, start_date, end_date)

    for symbol in buy_stocks:
        try:
            data = retriever.StockDataRetriever(symbol, buy_date, today)
            print(symbol + ": " + str(round(data.getHigh(0), 2)))
        except:
            continue
