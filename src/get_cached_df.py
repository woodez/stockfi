import pyarrow as pa
import pandas as pd
import redis
import pandas as pd
from io import StringIO
from datetime import date
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
import pyarrow as pa
import redis
import warnings
warnings.filterwarnings("ignore")


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

test = get_cached_df("woodez")
test["value"] = pd.to_numeric(test["value"], downcast="float")
test["date"] = pd.to_datetime(test["date"])
test = test.set_index(test["date"])
plt.plot(test)
plt.gcf().autofmt_xdate()
plt.show()