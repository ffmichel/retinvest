import pandas_datareader.data as web
import requests_cache
import datetime

EXPIRE_AFTER = datetime.timedelta(hours=3)
SESSION = requests_cache.CachedSession(
    cache_name='cache', backend='sqlite', expire_after=EXPIRE_AFTER)
SOURCE = 'yahoo'


def symbol_history(symbol, start_date, session=SESSION, source=SOURCE):
    ''' Collect symbol data. Results are cached using the sesseion. '''
    return web.DataReader(symbol, source, start=start_date, session=session)
