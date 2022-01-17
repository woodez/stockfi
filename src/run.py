import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
import redis
import pyarrow as pa
import warnings
warnings.filterwarnings("ignore")

# %matplotlib inlineimport redis
def get_cached_df(alias):

    pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
    cur = redis.Redis(connection_pool=pool)
    context = pa.default_serialization_context()
    all_keys = [key.decode("utf-8") for key in cur.keys()]

    if alias in all_keys:   
        result = cur.get(alias)

        dataframe = pd.DataFrame.from_dict(context.deserialize(result))

        return dataframe

    return None
many_years = 3
d = date.today()
year_back = d.replace(year=d.year - many_years).strftime("%Y-%m-%d")
today_date = d.strftime("%Y-%m-%d")
print('{0} and {1}'.format(today_date, year_back))

start = year_back
end = today_date
btc = yf.download('SQ',start,end)
eth = yf.download('ETH-CAD',start,end)
btc['MA200'] = btc['Open'].rolling(200).mean()

testing = btc['MA200'].tail(1).values[0]

print(btc.info())
test = get_cached_df("woodez")
test["value"] = pd.to_numeric(test["value"], downcast="float")
test["Datetime"] = pd.to_datetime(test["date"])
test = test.set_index('Datetime')
print(test.info())
###btc['Open'].plot(label = 'BTC', figsize = (15,7))
####plt.title('BTC')
btc['Open'].tail(60).plot(label = 'WOODEZ', figsize = (15,7))
plt.title('WOODEZ')
plt.show()