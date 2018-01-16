#!/usr/bin/env python
'''
Plot two symbols and their rolling correlation
side by side on the same graph.
'''
import argparse
import datetime

import pandas as pd
import bokeh.plotting as plt

from retinvest import data
from retinvest import time_series
from retinvest import visualize

START_DATE_DEFAULT = '1990-1-1'


def run(symbol1, symbol2, output_file, start_date, title):
    ''' Create symbols and correlation plot then save it. '''
    symbols = [symbol1, symbol2]
    growth_series = []
    for symbol in symbols:
        symbol_df = data.symbol_history(symbol, start_date)
        symbol_series = symbol_df['Close']
        growth = (symbol_series / symbol_series.iloc[0]) - 1.0
        growth.name = symbol
        growth_series.append(growth)

    correlation_series = time_series.correlate(*growth_series)

    growth_df = pd.concat(growth_series, axis=1)

    # output to static HTML file
    plt.output_file(output_file, title=title)

    fig = plt.figure(
        width=800,
        height=500,
        x_axis_type='datetime',
        title=title,
        tools=['pan,box_select,reset'])

    fig = visualize.plot_series(fig, growth_df)
    fig = visualize.plot_correlation(fig, correlation_series)

    # Add legends where we have the least clutter.
    fig.legend.location = 'top_left'
    plt.save(fig)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--symbol1', type=str, required=True)
    parser.add_argument('--symbol2', type=str, required=True)
    parser.add_argument(
        '-o',
        '--output',
        help='Output html file path.',
        type=str,
        required=True)
    parser.add_argument(
        '-s',
        '--start_date',
        help='Hyphen seperated date, as YYYY-MM-DD',
        type=str,
        default=START_DATE_DEFAULT)
    args = parser.parse_args()

    start_date = datetime.datetime(
        *[int(num) for num in args.start_date.split('-')])
    title = 'Correlation between {} and {} since {}'.format(
        args.symbol1, args.symbol2, start_date.strftime('%Y-%m-%d'))

    run(symbol1=args.symbol1,
        symbol2=args.symbol2,
        output_file=args.output,
        start_date=start_date,
        title=title)
