'''
Plot two symbols and their rolling correlation
side by side on the same graph.
'''
import argparse
import pandas_datareader.data as web
import bokeh.plotting as plt
import bokeh.palettes as pal
import bokeh.models as bmod
import datetime
import requests_cache
import numpy as np

EXPIRE_AFTER = datetime.timedelta(hours=3)
SESSION = requests_cache.CachedSession(
    cache_name='cache', backend='sqlite', expire_after=EXPIRE_AFTER)
SOURCE = 'yahoo'
START_DATE_DEFAULT = '1990-1-1'


def get_data(symbol, start_date, session=SESSION, source=SOURCE):
    ''' Collect symbol data. Results are cached using the sesseion. '''
    return web.DataReader(symbol, source, start=start_date, session=session)


def correlate(symbol1_series, symbol2_series, window=20):
    ''' Get coorelation between two time series as a pandas Dataframe. '''
    return symbol1_series.rolling(
        window=window, center=True).corr(symbol2_series)


def save_correlation_plot(series_list,
                          correlation,
                          plot_title,
                          output_file,
                          averaging_window=50):
    ''' Creates a figure with time series and  correlation plot and saves it.

    Args:
        series list: list of pandas.Dataframe.
        correlation: pandas dataframe containing a correlation time series.
        plot_title: str, title.
        output_file: str, path to the output file, as html.
        averaging_window: int, window over which the data is temporally smoothed out.
    '''
    # output to static HTML file
    plt.output_file(output_file)

    # create a datetime tooltip
    hover = bmod.HoverTool(
        line_policy='next',
        tooltips=[('date', '@date{%F}'), ('growth', '$y')],
        formatters={'date': 'datetime'},
    )

    fig = plt.figure(
        width=800,
        height=500,
        x_axis_type='datetime',
        title=plot_title,
        tools=['pan,box_select,reset', hover])

    for (series, series_name), color in zip(series_list, pal.Spectral11):
        # Rolling average of the series.
        series_avg = series.rolling(
            window=averaging_window, center=True).mean()

        source = plt.ColumnDataSource(
            data=dict(series_avg=series_avg, date=series_avg.index))
        fig.line(
            'date',
            'series_avg',
            source=source,
            legend=series_name,
            color=color)

    corr_avg = correlation.rolling(window=averaging_window, center=True).mean()

    # Do not show negative values in the positive part.
    corr_avg_pos = corr_avg.copy()
    corr_avg_pos[corr_avg_pos < 0] = np.nan

    # Do not show positive values in the negative part.
    corr_avg_neg = corr_avg.copy()
    corr_avg_neg[corr_avg_pos >= 0] = np.nan

    source = plt.ColumnDataSource(
        data=dict(
            series_avg=[corr_avg_pos, corr_avg_neg],
            date=[corr_avg_pos.index, corr_avg_neg.index],
            color=['green', 'red']))
    # add a line renderer with legend and line thickness
    fig.multi_line(
        'date',
        'series_avg',
        source=source,
        color='color',
        hover_line_color='color',
        legend='correlation')

    # Add legends where we have the least clutter.
    fig.legend.location = 'top_left'
    plt.save(fig)
    return None


def run(symbol1, symbol2, output_file, start_date, title):
    ''' Create symbols and correlation plot then save it. '''
    symbols = [symbol1, symbol2]
    growth_series = []
    for symbol in symbols:
        symbol_df = get_data(symbol, start_date)
        symbol_series = symbol_df['Close']
        growth_series.append((symbol_series / symbol_series.iloc[0]) - 1.0)

    correlation_series = correlate(*growth_series)
    save_correlation_plot(
        series_list=zip(*[growth_series, symbols]),
        correlation=correlation_series,
        plot_title=title,
        output_file=output_file)
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
