'''
Created on Jun 30, 2021

@author: FN-1776
'''

# Automatic detection line of support/resistance
# https://towardsdatascience.com/detection-of-price-support-and-resistance-levels-in-python-baedc44c34c9

# yfinance Tutorial
# https://algotrading101.com/learn/yfinance-guide/

import yfinance as yf
from datetime import datetime as dt


class StockDataRetriever:
    client = ""
    datetime_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%Y-%m-%d'

    def __init__(self, symbol, startDate, endDate):
        symbol = symbol.replace(".", "-")
        self.data = yf.Ticker(symbol).history(self, interval="1d", start=startDate, end=endDate)

    # Get data for 1 month, daily intervals
    def getData(self):
        return self.data

    def getHigh(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        return self.data.get('High')[daysAgo]

    def getLow(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        return self.data.get('Low')[daysAgo]

    def getOpen(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        return self.data.get('Open')[daysAgo]

    def getClose(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        return self.data.get('Close')[daysAgo]

    def getVolume(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        return self.data.get('Volume')[daysAgo]

    def getDate(self, daysAgo):
        if daysAgo is None:
            return None
        daysAgo = -1 * daysAgo
        date = self.data.index[daysAgo]
        return dt.strptime(str(date), BA_Retriever.datetime_format).date()

    def get_num_days_ago(self, date):
        list_dates = self.getData().index
        num_days = len(list_dates)
        search_date = dt.strptime(date, BA_Retriever.date_format).date()

        return BA_Retriever.__get_num_days_ago_binary_search(search_date, list_dates, 0, int(num_days - 1))

    @staticmethod
    def __get_num_days_ago_binary_search(search_date, list_dates, left, right):
        idx = int((left+right)/2)
        if idx >= len(list_dates):
            return None

        pivot_date = dt.strptime(str(list_dates[idx]), BA_Retriever.datetime_format).date()
        if left > right:
            return None

        if search_date < pivot_date:
            right = idx-1
            return BA_Retriever.__get_num_days_ago_binary_search(search_date, list_dates, left, right)
        elif search_date > pivot_date:
            left = idx+1
            return BA_Retriever.__get_num_days_ago_binary_search(search_date, list_dates, left, right)
        else:
            return len(list_dates)-idx


if __name__ == '__main__':
    BA_Retriever = StockDataRetriever("BA", "2021-05-01", "2021-06-02")
    print(BA_Retriever.getData().index)
    days_ago = BA_Retriever.get_num_days_ago("2021-05-14")
    print(BA_Retriever.getDate(days_ago))
