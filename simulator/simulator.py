import analysis.BullishDetector
from multiprocessing import Pool
import numpy as np
import time
from datetime import datetime as dt
import datetime
import retriever.StockDataRetriever as retriever
import analysis.LevelDetector as levels

sell_under_percentage = 0.9
sell_over_percentage = 1.05
date_format = '%Y-%m-%d'


def closest(lst, k):
    lst = np.asarray(lst)
    idx = (np.abs(lst - k)).argmin()
    return lst[idx]


def convert_to_datetime(date):
    return dt.strptime(date, date_format)


def add_day(date):
    additional_day = datetime.timedelta(days=1)
    return (convert_to_datetime(date) + additional_day).date()


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


def buy_stocks(stock_symbols, start_date, end_date):
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


def to_sell_stock(stock_symbol, buy_price, current_price, data):
    sell_under = buy_price * sell_under_percentage
    sell_over = buy_price * sell_over_percentage
    if current_price < sell_under or current_price > sell_over:
        return True
    else:
        return False


def sell_stock(stock_symbols, buy_price, start_date, last_sell_date):
    sellable = False


    # for daysAgo in range(1, len(data.getData())):
    #     close_today = data.getClose(daysAgo)
    #     if close_today < sell_low or close_today > sell_high:
    #         profit = round(close_today - buyPrice, 2)
    #         # print(f"{symbol} profit = {profit}")
    #         return profit

    return None


if __name__ == '__main__':
    stock_symbols = get_stock_symbols("test_stocks.txt")

    start_date = "2019-06-01"
    end_date = "2021-05-06"
    buy_date = "2021-05-06"
    today = "2021-9-13"
    # buy_stocks = buy_stocks(stock_symbols, start_date, end_date)
    total_profit = 0



    # for symbol in buy_stocks:
    #     try:
    #         # data = retriever.StockDataRetriever(symbol, buy_date, today)
    #         # buyPrice = round(data.getHigh(0), 2)
    #         # print(f"{symbol} bought at {buyPrice}")
    #
    #
    #
    #     except:
    #         continue
    print(f"Total Profit {total_profit}")
