import pyarrow as pa
import redis
import yfinance as yf

def cache_df(alias,df):
    pool = redis.ConnectionPool(host='192.168.2.233', port='6379', db=0)
    cur = redis.Redis(connection_pool=pool)
    context = pa.default_serialization_context()
    df_compressed =  context.serialize(df).to_buffer().to_pybytes()

    res = cur.set(alias,df_compressed)
    if res == True:
        print('df cached')


import_df = yf.download("TSLA","2015-01-01","2021-12-04")
cache_df("tsla", import_df)
