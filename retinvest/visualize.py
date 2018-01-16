import bokeh.models as bmod
import bokeh.palettes as pal
import bokeh.plotting as plt
import numpy as np

DEFAULT_AVERAGING_WINDOW = 50


def plot_series(fig,
                pandas_dataframe,
                averaging_window=DEFAULT_AVERAGING_WINDOW):
    ''' Add time series plots to the figure.

    The time series are assumed to be datetime indexed, and are
    averaged with a rolling time window.

    Args:
        fig: bokeh figure.
        pandas_dataframe: data frame indexed by datetime,
            each column is a new time series.
        averaging_window: width of the rolling time average window.
    Returns:
        Modified Bokeh figure.
    '''
    dates = pandas_dataframe.index
    for (series_name, series), color in zip(pandas_dataframe.iteritems(),
                                            pal.Spectral11):
        # Rolling average of the series.
        series_avg = series.rolling(
            window=averaging_window, center=True).mean()

        source = plt.ColumnDataSource(
            data=dict(series_avg=series_avg, date=dates))
        fig.line(
            'date',
            'series_avg',
            source=source,
            legend=series_name,
            color=color)

    # create a datetime tooltip
    hover = bmod.HoverTool(
        line_policy='next',
        tooltips=[('date', '@date{%F}'), ('growth', '$y')],
        formatters={'date': 'datetime'},
    )

    fig.add_tools(hover)
    return fig


def plot_correlation(fig,
                     correlation_series,
                     correlation_colors=['green', 'red'],
                     averaging_window=DEFAULT_AVERAGING_WINDOW):
    ''' Add colored correlation plots to the figure.

    The correlation will be displayes with two colors depending on its sign.
    The correlation time series is assumed to be datetime indexed, and is
    averaged with a rolling time window.

    Args:
        fig: bokeh figure.
        correlation_series: pandas series of corrleations.
        correlation_colors: list of colors representing positive and
            negative respectively.
        averaging_window: width of the rolling time average window.
    Returns:
        Modified Bokeh figure.
    '''
    corr_avg = correlation_series.rolling(
        window=averaging_window, center=True).mean()
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
        legend='Correlation')
    return fig
