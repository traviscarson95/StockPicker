# Automatic detection line of support/resistance
# https://towardsdatascience.com/detection-of-price-support-and-resistance-levels-in-python-baedc44c34c9

import retriever.StockDataRetriever as retriever
import pandas as pd
import numpy as np
import matplotlib as mpl_dates
import matplotlib as plt
from mplfinance import candlestick_ohlc


class LevelDetector:
    def __init__(self, stock_data_retriever):
        # Grab S&P 500 daily data
        self.stockDataRetriever = stock_data_retriever
        self.df = self.stockDataRetriever.data
        self.df['Date'] = pd.to_datetime(self.df.index)
        self.df['Date'] = self.df['Date'].apply(mpl_dates.date2num)
        self.df = self.df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        self.levels = []
        self.support_levels = []
        self.resistance_levels = []
        # Cleaning up noise; if a level is near another one, it will be discarded
        # Near is defined as less than the average candle size on the chart
        self.s = np.mean(self.df['High'] - self.df['Low'])
        self.find_levels()

    # These two functions identify 4-candles fractals
    @staticmethod
    def is_support(df, i):
        return df['Low'][i] < df['Low'][i - 1] < df['Low'][i - 2] and df['Low'][i] < df['Low'][i + 1] < df['Low'][i + 2]

    @staticmethod
    def is_resistance(df, i):
        return df['High'][i] > df['High'][i - 1] > df['High'][i - 2] and df['High'][i] > df['High'][i + 1] >\
               df['High'][i + 2]

    # Returns false if it is near some previously discovered key level
    def is_far_from_level(self, l):
        return np.sum([abs(l - x) < self.s for x in self.levels]) == 0

    # Finds all support and resistance levels and populates them to the class variables
    def find_levels(self):
        df = self.df
        # Create list that contains the support and resistance levels.
        # Each level is a tuple whose first element is the index of the signal candle
        # and the second element is price value.

        for i in range(2, df.shape[0] - 2):
            if LevelDetector.is_support(df, i):
                l = df['Low'][i]
                if self.is_far_from_level(l):
                    self.levels.append((i, l))
                    self.support_levels.append((i, l))
            elif LevelDetector.is_resistance(df, i):
                l = df['High'][i]
                if self.is_far_from_level(l):
                    self.levels.append((i, l))
                    self.resistance_levels.append((i, l))

    # Private method to plot price and key levels together
    def __plot_all(self, support_levels, resistance_levels):
        df = self.df

        # Plotting environment
        plt.rcParams['figure.figsize'] = [12, 7]
        plt.rc('font', size=14)

        fig = plt.figure()
        ax1 = plt.subplot()

        candlestick_ohlc(ax1, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

        date_format = mpl_dates.DateFormatter('%d %b %Y')
        ax1.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()

        for level in support_levels:
            plt.hlines(level[1], xmin=df['Date'][level[0]], xmax=max(df['Date']), colors='blue')
        for level in resistance_levels:
            plt.hlines(level[1], xmin=df['Date'][level[0]], xmax=max(df['Date']), colors='orange')

        plt.show()

    def get_support_levels(self):
        return self.support_levels

    # Return the prices for all support levels (excludes the date that the support level happened)
    def get_support_level_prices(self):
        return sorted([support_level[1] for support_level in self.get_support_levels()])

    def get_resistance_levels(self):
        return self.resistance_levels

    def plot_all_levels(self):
        self.__plot_all(self.support_levels, self.resistance_levels)

    def plot_support_levels(self):
        self.__plot_all(self.support_levels, [])

    def plot_resistance_levels(self):
        self.__plot_all([], self.resistance_levels)


if __name__ == '__main__':
    supportDetector = LevelDetector(retriever.StockDataRetriever("CNC", "2020-06-01", "2021-07-15"))
    supportDetector.get_support_level_prices()
    supportDetector.plot_all_levels()

    # print(supportDetector.getsupport_levels())
    # supportDetector.plotsupport_levels()
