import pyarrow as pa
import pandas as pd
import redis


def get_cached_df(alias):

    pool = redis.ConnectionPool(host='host',port='port', db=0) 
    cur = redis.Redis(connection_pool=pool)
    context = pa.default_serialization_context()
    all_keys = [key.decode("utf-8") for key in cur.keys()]

    if alias in all_keys:   
        result = cur.get(alias)

        dataframe = pd.DataFrame.from_dict(context.deserialize(result))

        return dataframe

    return None

print "{}".format(get_cached_df("tsla"))
