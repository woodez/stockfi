import pyarrow as pa
import pandas as pd
import redis


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

test = get_cached_df("woodez").tail(2)
latest = float(test['value'].values[1])
nextup = float(test['value'].values[0])
print(latest)
print(nextup)
if latest < nextup:
    print("Daily Trend is Down")
else:
    print("Daily Trend is Up")