'''
Time series operations.
'''


def correlate(symbol1_series, symbol2_series, window=20):
    ''' Get coorelation between two time series as a pandas Dataframe. '''
    return symbol1_series.rolling(
        window=window, center=True).corr(symbol2_series)
