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

    def __init__(self, symbol, startDate, endDate):
        symbol = symbol.replace(".", "-")
        self.data = yf.Ticker(symbol).history(self, interval="1d", start=startDate, end=endDate)

    # Get data for 1 month, daily intervals
    def getData(self):
        return self.data

    def getHigh(self, daysAgo):
        daysAgo = -1 * daysAgo
        return self.data.get('High')[daysAgo]

    def getLow(self, daysAgo):
        daysAgo = -1 * daysAgo
        return self.data.get('Low')[daysAgo]

    def getOpen(self, daysAgo):
        daysAgo = -1 * daysAgo
        return self.data.get('Open')[daysAgo]

    def getClose(self, daysAgo):
        daysAgo = -1 * daysAgo
        return self.data.get('Close')[daysAgo]

    def getVolume(self, daysAgo):
        daysAgo = -1 * daysAgo
        return self.data.get('Volume')[daysAgo]

    def getDate(self, daysAgo):
        daysAgo = -1 * daysAgo
        date = self.data.index[daysAgo]
        return dt.strptime(str(date), '%Y-%m-%d %H:%M:%S').date()


if __name__ == '__main__':
    BA_Retriever = StockDataRetriever("BA", "2021-05-01", "2021-06-02")
    print(BA_Retriever.getData())
    print(BA_Retriever.getHigh(1))
